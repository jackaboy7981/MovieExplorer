"""Application-wide exception handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
    """Handle known application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "error_code": exc.error_code,
            "status_code": exc.status_code,
        },
    )


async def general_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions with a generic 500 response."""
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "error_code": 500,
            "status_code": 500,
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    """Register global exception handlers."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
