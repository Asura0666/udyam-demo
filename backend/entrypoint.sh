#!/bin/bash
set -e

# Wait for Postgres to be ready
echo "Waiting for Postgres..."
sleep 5

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start FastAPI server
echo "Starting FastAPI..."
fastapi run ./src --host 0.0.0.0 --port 8000