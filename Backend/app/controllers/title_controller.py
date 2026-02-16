"""Title controller routes."""

from fastapi import APIRouter, Path

from app.core.api_docs import DEFAULT_ERROR_RESPONSES, ErrorResponse, TitleDetailsResponse
from app.core.exceptions import InvalidInputError

from app.service_logic.title_service_logic import (
    get_title_details as get_title_details_service,
)


router = APIRouter(prefix="/title", tags=["title"])


@router.get(
    "/{title_id}",
    response_model=TitleDetailsResponse,
    summary="Get Movie Details",
    description=(
        "Returns detailed information for one movie, including genres and contributors "
        "(actors/directors) with their roles."
    ),
    responses={
        **DEFAULT_ERROR_RESPONSES,
        404: {
            "model": ErrorResponse,
            "description": "Movie not found for the provided ID.",
        },
    },
)
def get_title_details(
    title_id: int = Path(
        ...,
        description="Movie identifier. Expected type: integer greater than 0.",
        examples=[10],
    )
) -> dict:
    """Return title details with contributors and their roles."""
    if not isinstance(title_id, int) or title_id <= 0:
        raise InvalidInputError("title ID")

    return get_title_details_service(title_id)
