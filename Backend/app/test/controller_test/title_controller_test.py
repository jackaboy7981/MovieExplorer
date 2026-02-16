"""Controller tests for title routes."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

import app.controllers.title_controller as title_controller
from app.core.exceptions import TitleNotFound
from app.core.handler import register_error_handlers


def _build_client() -> TestClient:
    app = FastAPI()
    register_error_handlers(app)
    app.include_router(title_controller.router)
    return TestClient(app)


def test_get_title_details_returns_service_payload(monkeypatch) -> None:
    """Valid title id should return service payload."""
    expected = {
        "id": 10,
        "title": "The Matrix",
        "release_year": 1999,
        "media_type": "movie",
        "genres": ["Action", "Sci-Fi"],
        "contributors": [],
    }

    def fake_get_title_details_service(title_id: int):
        assert title_id == 10
        return expected

    monkeypatch.setattr(
        title_controller,
        "get_title_details_service",
        fake_get_title_details_service,
    )
    client = _build_client()

    response = client.get("/title/10")

    assert response.status_code == 200
    assert response.json() == expected


def test_get_title_details_rejects_invalid_title_id() -> None:
    """Non-positive title id should return invalid input error."""
    client = _build_client()

    response = client.get("/title/0")

    assert response.status_code == 400
    assert response.json() == {
        "message": "Invalid input: title ID is invalid",
        "error_code": 1000,
        "status_code": 400,
    }


def test_get_title_details_handles_title_not_found(monkeypatch) -> None:
    """Service not-found exception should map to 404 response."""

    def fake_get_title_details_service(title_id: int):
        raise TitleNotFound(title_id)

    monkeypatch.setattr(
        title_controller,
        "get_title_details_service",
        fake_get_title_details_service,
    )
    client = _build_client()

    response = client.get("/title/999")

    assert response.status_code == 404
    assert response.json() == {
        "message": "Movie with ID 999 not found",
        "error_code": 1001,
        "status_code": 404,
    }
