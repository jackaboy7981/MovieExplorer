"""Contributor controller routes."""

from fastapi import APIRouter

from app.core.exceptions import InvalidInputError
from app.service_logic.contributor_service_logic import (
    get_contributor_details as get_contributor_details_service,
)

router = APIRouter(prefix="/contributor", tags=["contributor"])


@router.get("/{contributor_id}")
def get_contributor_details(contributor_id: int) -> dict:
    """Return contributor details with associated titles and roles."""
    if not isinstance(contributor_id, int) or contributor_id <= 0:
        raise InvalidInputError("contributor ID")

    return get_contributor_details_service(contributor_id)
