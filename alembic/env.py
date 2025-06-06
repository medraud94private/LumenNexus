# alembic/env.py
import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# ===== 여기가 중요 =====
# app.core.database에서 engine, Base, DATABASE_URL 임포트
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.core.database import Base, DATABASE_URL

# 동기용 URL 생성 (asyncpg 대신 postgres 사용)
SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

# 이 아래는 alembic 기본 자동 설정
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    # DB 연결 없이 SQL 파일 생성용, 동기 URL을 사용
    context.configure(
        url=SYNC_DATABASE_URL, 
        target_metadata=target_metadata, 
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # 실제 DB 연결 후 마이그레이션 진행, 동기 URL 사용
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        url=SYNC_DATABASE_URL,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
