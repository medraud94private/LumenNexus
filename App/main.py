import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker



# ──────────────
# 1) DB 설정
# ──────────────
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@db:5432/lumennexus"
)

SYNC_URL= DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


# ──────────────
# 2) Lifespan 컨텍스트 매니저
# ──────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 0.95+ 권장사항: lifespan 파라미터를 사용.
    앱 '시작 전'에 Alembic 마이그레이션 → '종료 후'에 리소스 정리.
    """


    # 필요시 DB 연결 테스트 등 추가 가능
    # 예: async with async_session() as session: ...

    # yield 한 뒤로 실제 요청 처리 시작
    yield

    # ------------------------------
    # 앱 종료 시: 리소스 정리
    # ------------------------------
    print(">>> [LIFESPAN] App shutting down. Disposing engine...")
    await engine.dispose()
    print(">>> [LIFESPAN] Cleanup complete.")

# ──────────────
# 3) FastAPI 앱 생성 + Lifespan 지정
# ──────────────
app = FastAPI(
    title="LumenNexus API",
    lifespan=lifespan
)

# ──────────────
# OpenAPI 스키마 오버라이드: local_kw 파라미터 제거
# ──────────────
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="0.1.0",
        description="LumenNexus API",
        routes=app.routes,
    )
    # 각 경로의 각 연산에서 'local_kw'라는 파라미터를 제거합니다.
    for path in openapi_schema.get("paths", {}).values():
        for operation in path.values():
            if "parameters" in operation:
                operation["parameters"] = [
                    param for param in operation["parameters"]
                    if param.get("name") != "local_kw"
                ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
# ──────────────
# 4) 라우터 등록 
# ──────────────
from app.api.card import router as card_router
app.include_router(card_router)

@app.get("/")
async def read_root():
    return {"message": "Hello, LumenNexus with Alembic + lifespan!"}

@app.get("/healthcheck")
async def healthcheck():
    """
    DB 연결 정상 여부를 확인하는 간단한 헬스체크 엔드포인트.
    """
    try:
        async with async_session() as session:
            result = await session.execute("SELECT 1")
            num = result.scalar()
            if num == 1:
                return {"db": "ok"}
    except Exception as e:
        return {"db": "error", "error": str(e)}
