from __future__ import annotations

from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .pipeline import PipelineRequest, run_pipeline


SCHEDULER: Optional[AsyncIOScheduler] = None


def get_scheduler() -> AsyncIOScheduler:
    global SCHEDULER
    if SCHEDULER is None:
        SCHEDULER = AsyncIOScheduler()
    return SCHEDULER


def ensure_scheduler_started() -> None:
    sch = get_scheduler()
    if not sch.running:
        sch.start()


def schedule_daily_pipeline(intent_text: str, hour: int = 0, minute: int = 0) -> str:
    ensure_scheduler_started()
    sch = get_scheduler()
    job = sch.add_job(lambda: run_pipeline(PipelineRequest(intent_text=intent_text)), 'cron', hour=hour, minute=minute)
    return job.id


