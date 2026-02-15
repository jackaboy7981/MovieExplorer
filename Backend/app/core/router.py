from fastapi import FastAPI

from app.controllers.browse_controller import router as browse_router
from app.controllers.contributor_controller import router as contributor_router
from app.controllers.title_controller import router as title_router


def register_routers(app: FastAPI) -> None:
    """Register all application routers in one place."""
    app.include_router(browse_router)
    app.include_router(title_router)
    app.include_router(contributor_router)
