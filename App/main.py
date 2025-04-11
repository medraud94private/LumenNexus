from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# DB 연결 URL은 docker-compose에서 정의한 환경변수와 일치시켜야 함.
DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/lumennexus"

# SQLAlchemy 비동기 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@app.get("/")
async def read_root():
    return {"message": "Hello, LumenNexus!"}

@app.get("/healthcheck")
async def healthcheck():
    # 데이터베이스 연결 확인 (간단히 SELECT 1 실행)
    try:
        async with async_session() as session:
            result = await session.execute("SELECT 1")
            num = result.scalar()
            if num == 1:
                return {"db": "ok"}
    except Exception as e:
        return {"db": "error", "error": str(e)}