"""Database connection pool lifecycle and helpers."""

from __future__ import annotations

import os

from psycopg2 import pool

from app.core.exceptions import ConnectionPoolNotInitializedError

connection_pool: pool.SimpleConnectionPool | None = None


def init_db() -> None:
    """Initialize the shared Postgres connection pool."""
    global connection_pool
    database_url = os.getenv("DATABASE_URL", "")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured.")

    connection_pool = pool.SimpleConnectionPool(1, 10, dsn=database_url)


def close_db() -> None:
    """Close all pooled connections."""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        connection_pool = None


def get_db_connection():
    """Get one connection from the pool."""
    if connection_pool is None:
        raise ConnectionPoolNotInitializedError()
    return connection_pool.getconn()
