#!/usr/bin/env sh
set -eu

echo "Running Alembic migrations..."
uv run alembic upgrade head

# the insert_csv_to_postgres check if the title or contributor table is empty if so inserts data from csv
echo "Seeding CSV data..."
uv run python app/scripts/insert_csv_to_postgres.py --database-url "$DATABASE_URL"

echo "Starting API server..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
