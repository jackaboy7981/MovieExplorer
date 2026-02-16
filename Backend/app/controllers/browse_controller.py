"""Browse controller routes."""

from __future__ import annotations

from datetime import datetime, UTC

from fastapi import APIRouter, Query

from app.core.exceptions import InvalidInputError
from app.service_logic.browse_service_logic import (
    browse_genres as browse_genres_service,
    browse_titles as browse_titles_service,
)

router = APIRouter(prefix="/browse", tags=["browse"])


@router.get("/genre")
def browse_genres() -> list[dict]:
    """Return available genres for browse filters."""
    return browse_genres_service()


@router.get("")
def browse_titles(
    offset: str | None = Query(None, description="Pagination offset"),
    page_size: str | None = Query(None, description="Pagination page size"),
    search_text: str | None = Query(None, description="Search text"),
    release_year: str | None = Query(None, description="Release year filter"),
    genre: str | None = Query(None, description="Genre ID filter"),
) -> dict:
    """Browse titles by optional search text and filters."""
    current_year = datetime.now(UTC).year
    parsed_offset = _parse_required_paging_value(offset, 0, "offset")
    parsed_page_size = _parse_required_paging_value(page_size, 10, "page_size")
    parsed_release_year = _parse_optional_int_value(release_year, "release_year")
    parsed_genre = _parse_optional_int_value(genre, "genre")

    if parsed_offset < 0:
        raise InvalidInputError("offset")
    if parsed_page_size <= 0:
        raise InvalidInputError("page_size")
    if parsed_release_year is not None and (
        parsed_release_year <= 0 or parsed_release_year >= current_year
    ):
        raise InvalidInputError("release_year")
    if parsed_genre is not None and parsed_genre <= 0:
        raise InvalidInputError("genre")

    normalized_search_text = search_text.strip() if search_text is not None else None
    if normalized_search_text == "":
        normalized_search_text = None

    return browse_titles_service(
        search_text=normalized_search_text,
        release_year=parsed_release_year,
        genre=parsed_genre,
        offset=parsed_offset,
        page_size=parsed_page_size,
    )


def _parse_required_paging_value(value: str | None, default: int, field_name: str) -> int:
    """Parse paging value with fallback default for missing/empty input."""
    if value is None or value.strip() == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise InvalidInputError(field_name) from exc


def _parse_optional_int_value(value: str | None, field_name: str) -> int | None:
    """Parse optional integer query value, treating missing/empty as None."""
    if value is None or value.strip() == "":
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise InvalidInputError(field_name) from exc
