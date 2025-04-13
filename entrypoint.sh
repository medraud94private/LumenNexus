#!/bin/sh
set -e

# -- 1) DB 준비 대기 --
echo "Waiting for PostgreSQL to be available..."
# docker-compose의 db 서비스 이름과 포트를 사용 (여기서는 'db'와 기본 5432)
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is available."

# -- 2) Alembic 마이그레이션 실행 --
echo "Running Alembic migrations..."
alembic upgrade head

# -- 3) FastAPI 서버 시작 --
echo "Starting FastAPI server..."
# uvicorn 경로는 main.py의 위치 및 애플리케이션 인스턴스 (예: app.main:app)에 맞게 지정합니다.
uvicorn app.main:app --host 0.0.0.0 --port 8000
