"""Service logic tests for title workflows."""

from __future__ import annotations

import pytest

from app.core.exceptions import TitleNotFound
import app.service_logic.title_service_logic as title_service_logic


def test_get_title_details_maps_title_genres_and_contributors(monkeypatch) -> None:
    """Title service should map provider data into API contract shape."""
    monkeypatch.setattr(
        title_service_logic,
        "fetch_title_by_id",
        lambda title_id: (10, "tt0133093", "The Matrix", 1999, "movie"),
    )
    monkeypatch.setattr(
        title_service_logic,
        "fetch_genres_by_title_id",
        lambda title_id: ["Action", "Sci-Fi"],
    )
    monkeypatch.setattr(
        title_service_logic,
        "fetch_contributors_by_title_id",
        lambda title_id: [
            (1, "nm0000206", "Keanu Reeves", "Actor"),
            (1, "nm0000206", "Keanu Reeves", "Actor"),
            (2, "nm0905154", "Lana Wachowski", "Director"),
            (2, "nm0905154", "Lana Wachowski", "Writer"),
        ],
    )

    result = title_service_logic.get_title_details(10)

    assert result == {
        "id": 10,
        "imdb_reference_id": "tt0133093",
        "title": "The Matrix",
        "release_year": 1999,
        "media_type": "movie",
        "genres": ["Action", "Sci-Fi"],
        "contributors": [
            {
                "id": 1,
                "imdb_reference_id": "nm0000206",
                "name": "Keanu Reeves",
                "roles": ["Actor"],
            },
            {
                "id": 2,
                "imdb_reference_id": "nm0905154",
                "name": "Lana Wachowski",
                "roles": ["Director", "Writer"],
            },
        ],
    }


def test_get_title_details_raises_not_found_when_title_missing(monkeypatch) -> None:
    """Missing title row should raise TitleNotFound."""
    monkeypatch.setattr(title_service_logic, "fetch_title_by_id", lambda _: None)

    with pytest.raises(TitleNotFound) as exc:
        title_service_logic.get_title_details(999)

    assert exc.value.message == "Movie with ID 999 not found"
