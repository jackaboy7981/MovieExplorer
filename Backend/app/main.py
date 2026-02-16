from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import config as _config
from app.core.db import close_db, init_db
from app.core.handler import register_error_handlers
from app.core.router import register_routers

app = FastAPI(
    title="MovieExplorer API",
    description=(
        "APIs to browse movies and genres, fetch detailed movie records, "
        "and fetch contributor (actor/director) profiles with related movies."
    ),
    version="1.0",
    docs_url="/docs" if _config.ENV == "dev" else None,
    openapi_tags=[
        {
            "name": "browse",
            "description": "Browse and search movie results with pagination and filters.",
        },
        {
            "name": "title",
            "description": "Movie-level detail APIs.",
        },
        {
            "name": "contributor",
            "description": "Contributor (actor/director) detail APIs.",
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)
register_routers(app)


@app.on_event("startup")
def startup() -> None:
    """Initialize DB resources when app starts."""
    init_db()


@app.on_event("shutdown")
def shutdown() -> None:
    """Release DB resources when app stops."""
    close_db()
