"""Controller tests for browse routes."""

from __future__ import annotations

from datetime import datetime, UTC

from fastapi import FastAPI
from fastapi.testclient import TestClient

import app.controllers.browse_controller as browse_controller
from app.core.handler import register_error_handlers


def _build_client() -> TestClient:
    app = FastAPI()
    register_error_handlers(app)
    app.include_router(browse_controller.router)
    return TestClient(app)


def test_browse_titles_with_valid_defaults(monkeypatch) -> None:
    """Returns service response and applies controller defaults."""
    captured: dict = {}

    def fake_browse_titles_service(**kwargs):
        captured.update(kwargs)
        return {"offset": 0, "page_size": 10, "results": []}

    monkeypatch.setattr(browse_controller, "browse_titles_service", fake_browse_titles_service)
    client = _build_client()

    response = client.get("/browse")

    assert response.status_code == 200
    assert response.json() == {"offset": 0, "page_size": 10, "results": []}
    assert captured == {
        "search_text": None,
        "release_year": None,
        "genre": None,
        "offset": 0,
        "page_size": 10,
    }


def test_browse_titles_normalizes_blank_search_text(monkeypatch) -> None:
    """Blank search text should be converted to None before service call."""
    captured: dict = {}

    def fake_browse_titles_service(**kwargs):
        captured.update(kwargs)
        return {"offset": 0, "page_size": 10, "results": []}

    monkeypatch.setattr(browse_controller, "browse_titles_service", fake_browse_titles_service)
    client = _build_client()

    response = client.get("/browse", params={"search_text": "   "})

    assert response.status_code == 200
    assert captured["search_text"] is None


def test_browse_titles_rejects_negative_offset() -> None:
    """Negative offset should return invalid input error."""
    client = _build_client()

    response = client.get("/browse", params={"offset": "-1"})

    assert response.status_code == 400
    assert response.json() == {
        "message": "Invalid input: offset is invalid",
        "error_code": 1000,
        "status_code": 400,
    }


def test_browse_titles_rejects_invalid_page_size() -> None:
    """Zero page size should return invalid input error."""
    client = _build_client()

    response = client.get("/browse", params={"page_size": "0"})

    assert response.status_code == 400
    assert response.json() == {
        "message": "Invalid input: page_size is invalid",
        "error_code": 1000,
        "status_code": 400,
    }


def test_browse_titles_rejects_page_size_above_limit() -> None:
    """Page size > 50 should return invalid input error."""
    client = _build_client()

    response = client.get("/browse", params={"page_size": "51"})

    assert response.status_code == 400
    assert response.json() == {
        "message": "Invalid input: page_size is invalid",
        "error_code": 1000,
        "status_code": 400,
    }


def test_browse_titles_rejects_release_year_not_less_than_current_year() -> None:
    """Release year must be less than current year."""
    client = _build_client()
    current_year = datetime.now(UTC).year

    response = client.get("/browse", params={"release_year": str(current_year)})

    assert response.status_code == 400
    assert response.json() == {
        "message": "Invalid input: release_year is invalid",
        "error_code": 1000,
        "status_code": 400,
    }


def test_browse_titles_rejects_invalid_genre() -> None:
    """Non-positive genre id should return invalid input error."""
    client = _build_client()

    response = client.get("/browse", params={"genre": "0"})

    assert response.status_code == 400
    assert response.json() == {
        "message": "Invalid input: genre is invalid",
        "error_code": 1000,
        "status_code": 400,
    }


def test_browse_titles_rejects_non_integer_offset() -> None:
    """Non-integer offset should return invalid input error."""
    client = _build_client()

    response = client.get("/browse", params={"offset": "abc"})

    assert response.status_code == 400
    assert response.json() == {
        "message": "Invalid input: offset is invalid",
        "error_code": 1000,
        "status_code": 400,
    }


def test_browse_genres_returns_service_payload(monkeypatch) -> None:
    """Genre endpoint should return genre list from service."""
    expected = [{"id": 1, "name": "Action"}, {"id": 2, "name": "Drama"}]

    def fake_browse_genres_service():
        return expected

    monkeypatch.setattr(browse_controller, "browse_genres_service", fake_browse_genres_service)
    client = _build_client()

    response = client.get("/browse/genres")

    assert response.status_code == 200
    assert response.json() == expected
