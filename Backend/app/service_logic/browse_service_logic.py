"""Service layer for browse workflows."""

from __future__ import annotations

from app.core.exceptions import InvalidInputError
from app.data_providers.browse_data_provider import fetch_browse_titles


def browse_titles(
    search_text: str | None,
    release_year: int | None,
    genre: int | None,
    offset: int,
    page_size: int,
) -> dict:
    """Return paginated titles matching browse criteria."""
    search_words = _tokenize_search_text(search_text)

    title_rows = fetch_browse_titles(
        search_words=search_words,
        release_year=release_year,
        genre_id=genre,
        offset=offset,
        page_size=page_size,
    )

    items = [
        {
            "id": row[0],
            "imdb_reference_id": row[1],
            "title": row[2],
            "release_year": row[3],
            "media_type": row[4],
        }
        for row in title_rows
    ]

    return {
        "offset": offset,
        "page_size": page_size,
        "results": items,
    }


def _tokenize_search_text(search_text: str | None) -> list[str]:
    """Split search text into words and validate token safety."""
    if search_text is None:
        return []

    tokens = [token.strip() for token in search_text.split() if token.strip()][:3]
    for token in tokens:
        if len(token) > 100:
            raise InvalidInputError("search_text")
        if "\x00" in token:
            raise InvalidInputError("search_text")
    return tokens