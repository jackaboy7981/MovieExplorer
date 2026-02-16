"""Controller tests for contributor routes."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

import app.controllers.contributor_controller as contributor_controller
from app.core.exceptions import ContributorNotFound
from app.core.handler import register_error_handlers


def _build_client() -> TestClient:
    app = FastAPI()
    register_error_handlers(app)
    app.include_router(contributor_controller.router)
    return TestClient(app)


def test_get_contributor_details_returns_service_payload(monkeypatch) -> None:
    """Valid contributor id should return service payload."""
    expected = {
        "id": 7,
        "name": "Keanu Reeves",
        "imdb_reference_id": "nm0000206",
        "titles": [],
    }

    def fake_get_contributor_details_service(contributor_id: int):
        assert contributor_id == 7
        return expected

    monkeypatch.setattr(
        contributor_controller,
        "get_contributor_details_service",
        fake_get_contributor_details_service,
    )
    client = _build_client()

    response = client.get("/contributor/7")

    assert response.status_code == 200
    assert response.json() == expected


def test_get_contributor_details_rejects_invalid_contributor_id() -> None:
    """Non-positive contributor id should return invalid input error."""
    client = _build_client()

    response = client.get("/contributor/0")

    assert response.status_code == 400
    assert response.json() == {
        "message": "Invalid input: contributor ID is invalid",
        "error_code": 1000,
        "status_code": 400,
    }


def test_get_contributor_details_handles_contributor_not_found(monkeypatch) -> None:
    """Service not-found exception should map to 404 response."""

    def fake_get_contributor_details_service(contributor_id: int):
        raise ContributorNotFound(contributor_id)

    monkeypatch.setattr(
        contributor_controller,
        "get_contributor_details_service",
        fake_get_contributor_details_service,
    )
    client = _build_client()

    response = client.get("/contributor/404")

    assert response.status_code == 404
    assert response.json() == {
        "message": "Contributor with ID 404 not found",
        "error_code": 1002,
        "status_code": 404,
    }
