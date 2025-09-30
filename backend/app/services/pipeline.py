from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional

import pandas as pd
from pydantic import BaseModel
from ..db.session import POOL, insert_run_start, update_run_finish
from .ch_client import write_dataframe as ch_write


class PipelineRequest(BaseModel):
    # Minimal request capturing intent and resources
    intent_text: Optional[str] = None
    steps: Optional[List[Dict[str, Any]]] = None
    schedule: Optional[str] = None  # e.g., "@daily"
    output: Optional[Dict[str, Any]] = None


async def create_pipeline_from_intent(req: PipelineRequest) -> Dict[str, Any]:
    # Use LLM to generate pipeline steps
    if req.intent_text:
        try:
            from .llm_client import llm_client
            # Parse intent with LLM
            intent_result = await llm_client.parse_intent(req.intent_text)
            # Generate steps based on intent (for now, use default profiles)
            steps = await llm_client.generate_pipeline_steps(intent_result, [])
            return {"steps": steps, "schedule": req.schedule or intent_result.get("schedule", "@daily")}
        except Exception:
            # Fallback to simple rule-based parsing
            steps: List[Dict[str, Any]] = [
                {"op": "read_csv", "name": "csv"},
                {"op": "trim_strings", "input": "csv"},
                {"op": "read_json", "name": "json"},
                {"op": "join", "left": "csv", "right": "json", "on": "user_id"},
                {"op": "aggregate", "by": "user_id", "metric": "avg", "column": "amount", "alias": "avg_check"},
                {"op": "write_postgres", "table": "test.etl_result"},
            ]
            return {"steps": steps, "schedule": req.schedule or "@daily"}
    return {"steps": req.steps or [], "schedule": req.schedule}


def _trim_strings(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype("string").str.strip()
    return df


async def run_pipeline(req: PipelineRequest) -> Dict[str, Any]:
    # Minimal in-memory engine for demo
    context: Dict[str, pd.DataFrame] = {}
    steps = req.steps or (await create_pipeline_from_intent(req))["steps"]
    run_id: Optional[int] = None

    try:
        # Start run log if DB available
        try:
            run_id = await insert_run_start("in_memory_demo")
        except Exception:
            run_id = None

        for step in steps:
            op = step.get("op")
            if op == "read_csv":
                path = step.get("path", "./data/input.csv")
                context[step.get("name", "csv")] = pd.read_csv(path)
            elif op == "read_json":
                path = step.get("path", "./data/input.json")
                context[step.get("name", "json")] = pd.read_json(path, lines=False)
            elif op == "trim_strings":
                src = step.get("input") or "csv"
                context[src] = _trim_strings(context[src])
            elif op == "join":
                left = context[step.get("left", "csv")]
                right = context[step.get("right", "json")]
                on = step.get("on", "user_id")
                context["joined"] = left.merge(right, on=on, how="left")
            elif op == "aggregate":
                df = context.get("joined")
                by = step.get("by", "user_id")
                metric = step.get("metric", "avg")
                column = step.get("column", "amount")
                alias = step.get("alias", f"{metric}_{column}")
                if metric == "avg":
                    agg = df.groupby(by)[column].mean().reset_index(name=alias)
                else:
                    raise ValueError("Unsupported metric")
                context["result"] = agg
            elif op == "write_postgres":
                table = step.get("table", "result")
                out_path = f"./data/{table.replace('.', '_')}.csv"
                context.get("result", list(context.values())[-1]).to_csv(out_path, index=False)
            elif op == "write_clickhouse":
                table = step.get("table", "default.etl_result")
                df = context.get("result", list(context.values())[-1])
                ch_write(df, table)
            else:
                raise ValueError(f"Unsupported op: {op}")

        head_preview = context.get("result", list(context.values())[-1]).head(10).to_dict(orient="records")
        if run_id is not None:
            await update_run_finish(run_id, "success")
        return {"status": "ok", "preview": head_preview}
    except Exception as e:
        if run_id is not None:
            try:
                await update_run_finish(run_id, "failed")
            except Exception:
                pass
        raise



