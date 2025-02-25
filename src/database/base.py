from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config.settings import settings


engine = create_async_engine(settings.db_uri)
async_session = async_sessionmaker(engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    ...