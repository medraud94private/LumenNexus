import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Alembic
from alembic.config import Config
from alembic import command

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

# Alembic.ini 경로(본 예시에선 main.py와 같은 디렉토리에 있다고 가정)
ALEMBIC_INI_PATH = os.path.join(os.path.dirname(__file__), "..", "alembic.ini")

def run_alembic_migrations_sync():
    """
    동기 방식으로 Alembic 마이그레이션 수행하는 함수.
    (asynccontextmanager 내부가 아닌, 별도 동기 함수)
    """
    print(">>> [ALEMBIC] Using SYNC_URL =", SYNC_URL)
    alembic_cfg = Config(ALEMBIC_INI_PATH)
    alembic_cfg.set_main_option("sqlalchemy.url", SYNC_URL)
    command.upgrade(alembic_cfg, "head")

# ──────────────
# 2) Lifespan 컨텍스트 매니저
# ──────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 0.95+ 권장사항: lifespan 파라미터를 사용.
    앱 '시작 전'에 Alembic 마이그레이션 → '종료 후'에 리소스 정리.
    """
    # ------------------------------
    # 앱 시작 전: DB 마이그레이션
    # ------------------------------
    try:
        print(">>> [LIFESPAN] Running Alembic migrations in threadpool...")
        await run_in_threadpool(run_alembic_migrations_sync)
        print(">>> [LIFESPAN] Migrations complete. DB is up to date.")
    except Exception as e:
        print(">>> [LIFESPAN] Migration ERROR:", e)
        # 마이그레이션 실패 시 앱 시작을 중지시킬지 여부는 상황에 따라 결정
        raise

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
