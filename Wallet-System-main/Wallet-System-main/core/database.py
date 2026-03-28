import os 
from typing import AsyncGenerator
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


load_dotenv(override=True)

URI = os.getenv("DB_URI")

# Engine with max 30 connection at max other will until completed 
engine = create_async_engine(
                    URI, 
                    pool_pre_ping=True,
                    pool_size = 20, 
                    max_overflow=10,
                )

# Async Session
SessionLocal = sessionmaker(
                    bind=engine,
                    autoflush=False, 
                    expire_on_commit=False, 
                    class_=AsyncSession
                )

# Async Context Manager allows I/O suspension and concurrency. Also takes care of connection close 
# Seperate use for Service or Repo Layer
@asynccontextmanager
async def get_connection():
    async with SessionLocal() as session:
        yield session

# Async Session, Useed for Controller layer FastApi 
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
