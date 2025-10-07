from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings
import ssl
from sqlalchemy.pool import NullPool
import logging
mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB_NAME]


connect_args = {"statement_cache_size": 0}

engine = create_async_engine(
    str(settings.ASYNC_DATABASE_URL),
    poolclass=NullPool,
    connect_args=connect_args,  
    execution_options={"compiled_cache": None},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with SessionLocal() as session:
        yield session