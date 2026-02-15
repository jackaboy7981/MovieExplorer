"""Data access layer for browse reads."""

from __future__ import annotations

from app.core import db
from app.core.exceptions import DataProviderError


def fetch_browse_titles(
    search_words: list[str],
    release_year: int | None,
    genre_id: int | None,
    offset: int,
    page_size: int,
) -> list[tuple]:
    """Fetch paginated titles based on search words and filters."""
    conn = db.get_db_connection()
    try:
        with conn.cursor() as cur:
            query = """
                SELECT DISTINCT t.id, t.imdb_reference_id, t.title, t.release_year, mt.name
                FROM title t
                JOIN media_type_lkup mt ON mt.id = t.media_type
                LEFT JOIN contributor_title_mapping ctm ON ctm.title_id = t.id
                LEFT JOIN contributor c ON c.id = ctm.contributor_id
                LEFT JOIN title_genre tg ON tg.title_id = t.id
                LEFT JOIN genre_type_lkup g ON g.id = tg.genre_id
            """

            where_clauses: list[str] = []
            params: list[object] = []

            if search_words:
                for word in search_words:
                    pattern = f"%{word}%"
                    where_clauses.append(
                        """
                        (
                            t.title ILIKE %s
                            OR c.name ILIKE %s
                            OR g.name ILIKE %s
                            OR CAST(t.release_year AS TEXT) ILIKE %s
                        )
                        """
                    )
                    params.extend([pattern, pattern, pattern, pattern])

            if release_year is not None:
                where_clauses.append("t.release_year = %s")
                params.append(release_year)

            if genre_id is not None:
                where_clauses.append(
                    """
                    EXISTS (
                        SELECT 1
                        FROM title_genre tg2
                        WHERE tg2.title_id = t.id AND tg2.genre_id = %s
                    )
                    """
                )
                params.append(genre_id)

            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

            query += " ORDER BY t.title, t.id LIMIT %s OFFSET %s"
            params.extend([page_size, offset])

            cur.execute(query, tuple(params))
            rows = cur.fetchall()
    except Exception as exc:
        raise DataProviderError() from exc
    finally:
        if conn is not None and db.connection_pool is not None:
            db.connection_pool.putconn(conn)

    return rows
