"""Browse controller routes."""

from __future__ import annotations

from datetime import datetime, UTC

from fastapi import APIRouter, Query

from app.core.api_docs import (
    BrowseGenreResponse,
    BrowseTitlesResponse,
    DEFAULT_ERROR_RESPONSES,
    ErrorResponse,
)
from app.core.exceptions import InvalidInputError
from app.service_logic.browse_service_logic import (
    browse_genres as browse_genres_service,
    browse_titles as browse_titles_service,
)

router = APIRouter(prefix="/browse", tags=["browse"])
MAX_PAGE_SIZE = 50


@router.get(
    "/genres",
    response_model=list[BrowseGenreResponse],
    summary="List Browse Genres",
    description=(
        "Returns all genres available for filtering movie browse/search results. "
        "Use the returned `id` as the `genre` query parameter in `GET /browse`."
    ),
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal server error.",
        }
    },
)
def browse_genres() -> list[dict]:
    """Return available genres for browse filters."""
    return browse_genres_service()


@router.get(
    "",
    response_model=BrowseTitlesResponse,
    summary="Browse Movies",
    description=(
        "Returns a paginated movie list. Supports free-text search across movie titles, "
        "contributors, genres, and release year text, with optional structured filters."
    ),
    responses=DEFAULT_ERROR_RESPONSES,
)
def browse_titles(
    offset: str | None = Query(
        None,
        description="Pagination offset. Expected type: integer. Defaults to 0.",
        examples=["0"],
    ),
    page_size: str | None = Query(
        None,
        description=(
            "Page size. Expected type: integer. Defaults to 10. "
            "Accepted range: 1 to 50."
        ),
        examples=["28"],
    ),
    search_text: str | None = Query(
        None,
        description=(
            "Optional free-text query. Search tokens are matched against movie title, "
            "contributor name, genre name, and release year text."
        ),
        examples=["matrix keanu"],
    ),
    release_year: str | None = Query(
        None,
        description=(
            "Optional release year filter. Expected type: integer. "
            "Must be less than the current year."
        ),
        examples=["1999"],
    ),
    genre: str | None = Query(
        None,
        description="Optional genre filter. Expected type: integer genre ID.",
        examples=["1"],
    ),
) -> dict:
    """Browse titles by optional search text and filters."""
    current_year = datetime.now(UTC).year
    parsed_offset = _parse_required_paging_value(offset, 0, "offset")
    parsed_page_size = _parse_required_paging_value(page_size, 10, "page_size")
    parsed_release_year = _parse_optional_int_value(release_year, "release_year")
    parsed_genre = _parse_optional_int_value(genre, "genre")

    if parsed_offset < 0:
        raise InvalidInputError("offset")
    if parsed_page_size <= 0 or parsed_page_size > MAX_PAGE_SIZE:
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
