from fastapi import FastAPI
from pytz import utc
from src.logic.uploading_data import upload_data
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.config.logger_ import init


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    scheduler = AsyncIOScheduler()
    scheduler.configure(timezone=utc)
    scheduler.add_job(
        func=upload_data,
        trigger='cron',
        hour='23',
        minute='50'
    )
    scheduler.start()
    yield
    await scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
