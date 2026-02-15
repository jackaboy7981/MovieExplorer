"""Title controller routes."""

from fastapi import APIRouter

from app.core.exceptions import AppException, InvalidInputError, TitleNotFound

from app.service_logic.title_service_logic import (
    get_title_details as get_title_details_service,
)


router = APIRouter(prefix="/title", tags=["title"])


@router.get("/{title_id}")
def get_title_details(title_id: int) -> dict:
    """Return title details with contributors and their roles."""
    if not isinstance(title_id, int) or title_id <= 0:
        raise InvalidInputError("title ID")

    return get_title_details_service(title_id)

