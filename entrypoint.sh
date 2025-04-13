#!/bin/sh
set -e

echo "Waiting for PostgreSQL to be available..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is available."

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
