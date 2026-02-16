"""Service logic tests for contributor workflows."""

from __future__ import annotations

import pytest

from app.core.exceptions import ContributorNotFound
import app.service_logic.contributor_service_logic as contributor_service_logic


def test_get_contributor_details_maps_contributor_and_titles(monkeypatch) -> None:
    """Contributor service should map provider rows and merge duplicate roles."""
    monkeypatch.setattr(
        contributor_service_logic,
        "fetch_contributor_by_id",
        lambda contributor_id: (7, "nm0000206", "Keanu Reeves"),
    )
    monkeypatch.setattr(
        contributor_service_logic,
        "fetch_titles_by_contributor_id",
        lambda contributor_id: [
            (10, "tt0133093", "The Matrix", 1999, "movie", "Actor"),
            (10, "tt0133093", "The Matrix", 1999, "movie", "Actor"),
            (11, "tt0234215", "The Matrix Reloaded", 2003, "movie", "Actor"),
        ],
    )

    result = contributor_service_logic.get_contributor_details(7)

    assert result == {
        "id": 7,
        "imdb_reference_id": "nm0000206",
        "name": "Keanu Reeves",
        "titles": [
            {
                "id": 10,
                "imdb_reference_id": "tt0133093",
                "title": "The Matrix",
                "release_year": 1999,
                "media_type": "movie",
                "roles": ["Actor"],
            },
            {
                "id": 11,
                "imdb_reference_id": "tt0234215",
                "title": "The Matrix Reloaded",
                "release_year": 2003,
                "media_type": "movie",
                "roles": ["Actor"],
            },
        ],
    }


def test_get_contributor_details_raises_not_found_when_missing(monkeypatch) -> None:
    """Missing contributor row should raise ContributorNotFound."""
    monkeypatch.setattr(contributor_service_logic, "fetch_contributor_by_id", lambda _: None)

    with pytest.raises(ContributorNotFound) as exc:
        contributor_service_logic.get_contributor_details(404)

    assert exc.value.message == "Contributor with ID 404 not found"
