"""Service logic tests for browse workflows."""

from __future__ import annotations

import pytest

from app.core.exceptions import InvalidInputError
import app.service_logic.browse_service_logic as browse_service_logic


def test_browse_titles_maps_rows_and_passes_expected_params(monkeypatch) -> None:
    """browse_titles should map provider rows and pass parsed search words."""
    captured: dict = {}

    def fake_fetch_browse_titles(**kwargs):
        captured.update(kwargs)
        return [
            (1, "tt0000001", "Movie One", 1999, "movie"),
            (2, "tt0000002", "Movie Two", 2001, "movie"),
        ]

    monkeypatch.setattr(browse_service_logic, "fetch_browse_titles", fake_fetch_browse_titles)

    result = browse_service_logic.browse_titles(
        search_text="tom hanks drama extra-word",
        release_year=1999,
        genre=2,
        offset=28,
        page_size=28,
    )

    assert captured == {
        "search_words": ["tom", "hanks", "drama"],
        "release_year": 1999,
        "genre_id": 2,
        "offset": 28,
        "page_size": 28,
    }
    assert result == {
        "offset": 28,
        "page_size": 28,
        "results": [
            {
                "id": 1,
                "imdb_reference_id": "tt0000001",
                "title": "Movie One",
                "release_year": 1999,
                "media_type": "movie",
            },
            {
                "id": 2,
                "imdb_reference_id": "tt0000002",
                "title": "Movie Two",
                "release_year": 2001,
                "media_type": "movie",
            },
        ],
    }


def test_browse_titles_rejects_too_long_search_token() -> None:
    """Token length > 100 should raise InvalidInputError."""
    invalid_search_text = "a" * 101

    with pytest.raises(InvalidInputError) as exc:
        browse_service_logic.browse_titles(
            search_text=invalid_search_text,
            release_year=None,
            genre=None,
            offset=0,
            page_size=10,
        )

    assert exc.value.message == "Invalid input: search_text is invalid"


def test_browse_titles_rejects_search_with_null_byte() -> None:
    """Null byte in search token should raise InvalidInputError."""
    with pytest.raises(InvalidInputError) as exc:
        browse_service_logic.browse_titles(
            search_text="bad\x00token",
            release_year=None,
            genre=None,
            offset=0,
            page_size=10,
        )

    assert exc.value.message == "Invalid input: search_text is invalid"


def test_browse_genres_returns_provider_payload(monkeypatch) -> None:
    """browse_genres should pass through provider genres."""
    expected = [{"id": 1, "name": "Action"}, {"id": 2, "name": "Drama"}]

    monkeypatch.setattr(browse_service_logic, "fetch_browse_genres", lambda: expected)

    assert browse_service_logic.browse_genres() == expected
