import asyncio
import os
from typing import List

from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .services.profiling import profile_datasets
from .services.pipeline import PipelineRequest, create_pipeline_from_intent, run_pipeline
from .services.intent import parse_intent
from .db.session import init_db
from .services import vector as vector_store
from .db.session import fetch_recent_runs
from .services.reco import recommend_storage, generate_postgres_ddl, generate_clickhouse_ddl
from .services.scheduler import schedule_daily_pipeline, ensure_scheduler_started
from .services.airflow_export import dag_from_steps
from .services.semantic_join import suggest_join_keys, build_data_contract


class HealthResponse(BaseModel):
    status: str


def create_app() -> FastAPI:
    app = FastAPI(title="DataEngineer AI", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def on_startup() -> None:
        await init_db()
        ensure_scheduler_started()

    @app.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(status="ok")

    @app.post("/upload/profile")
    async def upload_and_profile(files: List[UploadFile] = File(...)):
        profiles = await profile_datasets(files)
        return JSONResponse(content={"profiles": profiles})

    @app.post("/reco/storage")
    async def reco_storage(payload: dict):
        profile = payload.get("profile", {})
        return recommend_storage(profile)

    @app.post("/ddl/generate")
    async def ddl_generate(payload: dict):
        system = (payload.get("system") or "postgres").lower()
        table = payload.get("table", "public.generated_table")
        columns_info = payload.get("columns_info", {})
        if system in ("postgres", "postgresql"):
            return {"ddl": generate_postgres_ddl(table, columns_info)}
        if system in ("clickhouse", "ch"):
            return {"ddl": generate_clickhouse_ddl(table, columns_info)}
        return JSONResponse(status_code=400, content={"error": "Unsupported system"})

    @app.post("/intent/parse")
    async def intent_parse(payload: dict):
        text = payload.get("text", "")
        result = await parse_intent(text)
        return JSONResponse(content=result)

    @app.post("/vector/upsert")
    async def vector_upsert(payload: dict):
        namespace = payload.get("namespace", "default")
        doc_id = payload.get("id") or payload.get("doc_id") or "doc"
        text = payload.get("text", "")
        metadata = payload.get("metadata", {})
        vector_store.upsert(namespace, doc_id, text, metadata)
        return {"status": "ok"}

    @app.post("/vector/search")
    async def vector_search(payload: dict):
        namespace = payload.get("namespace", "default")
        query = payload.get("query", "")
        top_k = int(payload.get("top_k", 5))
        return {"results": vector_store.search(namespace, query, top_k)}

    @app.post("/semantic/join_suggest")
    async def semantic_join(payload: dict):
        left = payload.get("left_profile", {})
        right = payload.get("right_profile", {})
        return {"suggestions": suggest_join_keys(left, right)}

    @app.post("/contract/build")
    async def contract_build(payload: dict):
        profile = payload.get("profile", {})
        return build_data_contract(profile)

    @app.post("/chat/assistant")
    async def chat_assistant(payload: dict):
        from .services.llm_client import llm_client
        message = payload.get("message", "")
        response = await llm_client.generate_response(message)
        return {"response": response}

    @app.post("/pipeline/plan")
    async def pipeline_plan(req: PipelineRequest):
        plan = await create_pipeline_from_intent(req)
        return JSONResponse(content=plan)

    @app.post("/pipeline/run")
    async def pipeline_run(req: PipelineRequest):
        result = await run_pipeline(req)
        return JSONResponse(content=result)

    @app.post("/airflow/export")
    async def airflow_export(req: PipelineRequest):
        plan = await create_pipeline_from_intent(req)
        dag_code = dag_from_steps(dag_id="generated_etl", steps=plan.get("steps", []))
        return {"dag.py": dag_code}

    @app.get("/runs/recent")
    async def runs_recent(limit: int = 50):
        runs = await fetch_recent_runs(limit=limit)
        return {"runs": runs}

    @app.post("/schedule/daily")
    async def schedule_daily(payload: dict):
        intent_text = payload.get("intent_text", "etl по user_id")
        hour = int(payload.get("hour", 0))
        minute = int(payload.get("minute", 0))
        job_id = schedule_daily_pipeline(intent_text=intent_text, hour=hour, minute=minute)
        return {"job_id": job_id}

    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):
        await ws.accept()
        try:
            while True:
                msg = await ws.receive_text()
                await ws.send_text(f"echo: {msg}")
        except WebSocketDisconnect:
            pass

    return app


app = create_app()


