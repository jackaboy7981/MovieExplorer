"""Data access layer for title-related reads."""

from __future__ import annotations

from app.core import db
from app.core.exceptions import DataProviderError


def fetch_title_by_id(title_id: int) -> tuple | None:
    """Fetch title row by id."""
    conn = db.get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT t.id, t.imdb_reference_id, t.title, t.release_year, mt.name
                FROM title t
                JOIN media_type_lkup mt ON mt.id = t.media_type
                WHERE t.id = %s
                LIMIT 1
                """,
                (title_id,),
            )
            title_row = cur.fetchone()
    except Exception as exc:
        raise DataProviderError() from exc
    finally:
        if conn is not None and db.connection_pool is not None:
            db.connection_pool.putconn(conn)

    return title_row


def fetch_genres_by_title_id(title_id: int) -> list[str]:
    """Fetch genre names for a title."""
    conn = db.get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT g.name
                FROM title_genre tg
                JOIN genre_type_lkup g ON g.id = tg.genre_id
                WHERE tg.title_id = %s
                ORDER BY g.name
                """,
                (title_id,),
            )
            genre_rows = cur.fetchall()
    except Exception as exc:
        raise DataProviderError() from exc
    finally:
        if conn is not None and db.connection_pool is not None:
            db.connection_pool.putconn(conn)

    return [row[0] for row in genre_rows]


def fetch_titles_by_contributor_id(contributor_id: int) -> list[tuple]:
    """Fetch title-role rows for a contributor."""
    conn = db.get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT t.id, t.imdb_reference_id, t.title, t.release_year, mt.name, ctl.name
                FROM contributor_title_mapping ctm
                JOIN title t ON t.id = ctm.title_id
                JOIN media_type_lkup mt ON mt.id = t.media_type
                JOIN contributor_type_lkup ctl ON ctl.id = ctm.type_id
                WHERE ctm.contributor_id = %s
                ORDER BY t.title, ctl.name
                """,
                (contributor_id,),
            )
            title_rows = cur.fetchall()
    except Exception as exc:
        raise DataProviderError() from exc
    finally:
        if conn is not None and db.connection_pool is not None:
            db.connection_pool.putconn(conn)

    return title_rows
