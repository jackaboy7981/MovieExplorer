"""Contributor controller routes."""

from fastapi import APIRouter, Path

from app.core.api_docs import (
    ContributorDetailsResponse,
    DEFAULT_ERROR_RESPONSES,
    ErrorResponse,
)
from app.core.exceptions import InvalidInputError
from app.service_logic.contributor_service_logic import (
    get_contributor_details as get_contributor_details_service,
)

router = APIRouter(prefix="/contributor", tags=["contributor"])


@router.get(
    "/{contributor_id}",
    response_model=ContributorDetailsResponse,
    summary="Get Contributor Details",
    description=(
        "Returns detailed information for one contributor (actor/director), including "
        "all related movies and role names for each movie."
    ),
    responses={
        **DEFAULT_ERROR_RESPONSES,
        404: {
            "model": ErrorResponse,
            "description": "Contributor not found for the provided ID.",
        },
    },
)
def get_contributor_details(
    contributor_id: int = Path(
        ...,
        description="Contributor identifier. Expected type: integer greater than 0.",
        examples=[7],
    )
) -> dict:
    """Return contributor details with associated titles and roles."""
    if not isinstance(contributor_id, int) or contributor_id <= 0:
        raise InvalidInputError("contributor ID")

    return get_contributor_details_service(contributor_id)
