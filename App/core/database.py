# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/lumennexus"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

class Base(DeclarativeBase):
    pass

# 데이터베이스 세션 의존성 함수 작성
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session