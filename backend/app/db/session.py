import os
from typing import Any

import asyncpg


POOL: Any = None


async def init_db() -> None:
    global POOL
    dsn = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@postgres:5432/metadata",
    )
    try:
        POOL = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=5)
        async with POOL.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id SERIAL PRIMARY KEY,
                    pipeline TEXT,
                    status TEXT,
                    started_at TIMESTAMP DEFAULT NOW(),
                    finished_at TIMESTAMP
                );
                """
            )
    except Exception:
        # In local dev without DB, continue
        POOL = None


async def insert_run_start(pipeline_name: str) -> int | None:
    if POOL is None:
        return None
    async with POOL.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO runs (pipeline, status, started_at) VALUES ($1, $2, NOW()) RETURNING id",
            pipeline_name,
            "running",
        )
        return int(row["id"]) if row else None


async def update_run_finish(run_id: int, status: str) -> None:
    if POOL is None:
        return
    async with POOL.acquire() as conn:
        await conn.execute(
            "UPDATE runs SET status=$1, finished_at=NOW() WHERE id=$2",
            status,
            run_id,
        )


async def fetch_recent_runs(limit: int = 50) -> list[dict[str, Any]]:
    if POOL is None:
        return []
    async with POOL.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, pipeline, status, started_at, finished_at FROM runs ORDER BY id DESC LIMIT $1",
            limit,
        )
    return [dict(r) for r in rows]


