"""Data access layer for contributor-related reads."""

from __future__ import annotations

from app.core import db
from app.core.exceptions import DataProviderError


def fetch_contributor_by_id(contributor_id: int) -> tuple | None:
    """Fetch contributor row by id."""
    conn = db.get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.id, c.imdb_reference_id, c.name
                FROM contributor c
                WHERE c.id = %s
                LIMIT 1
                """,
                (contributor_id,),
            )
            contributor_row = cur.fetchone()
    except Exception as exc:
        raise DataProviderError() from exc
    finally:
        if conn is not None and db.connection_pool is not None:
            db.connection_pool.putconn(conn)

    return contributor_row


def fetch_contributors_by_title_id(title_id: int) -> list[tuple]:
    """Fetch contributor-role rows for a title."""
    conn = db.get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.id, c.imdb_reference_id, c.name, ctl.name
                FROM contributor_title_mapping ctm
                JOIN contributor c ON c.id = ctm.contributor_id
                JOIN contributor_type_lkup ctl ON ctl.id = ctm.type_id
                WHERE ctm.title_id = %s
                ORDER BY c.name, ctl.name
                """,
                (title_id,),
            )
            contributor_rows = cur.fetchall()
    except Exception as exc:
        raise DataProviderError() from exc
    finally:
        if conn is not None and db.connection_pool is not None:
            db.connection_pool.putconn(conn)

    return contributor_rows
