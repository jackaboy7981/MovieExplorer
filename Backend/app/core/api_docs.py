"""OpenAPI response models and reusable response docs."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error payload returned by global exception handlers."""

    message: str = Field(..., examples=["Invalid input: page_size is invalid"])
    error_code: int = Field(..., examples=[1000])
    status_code: int = Field(..., examples=[400])


class BrowseTitleItemResponse(BaseModel):
    """One title row in browse results."""

    id: int = Field(..., examples=[10])
    imdb_reference_id: str | None = Field(..., examples=["tt0133093"])
    title: str = Field(..., examples=["The Matrix"])
    release_year: int | None = Field(..., examples=[1999])
    media_type: str = Field(..., examples=["movie"])


class BrowseTitlesResponse(BaseModel):
    """Paginated browse response."""

    offset: int = Field(..., examples=[0])
    page_size: int = Field(..., examples=[28])
    results: list[BrowseTitleItemResponse]


class BrowseGenreResponse(BaseModel):
    """Genre option for browse filtering."""

    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Action"])


class ContributorSummaryResponse(BaseModel):
    """Contributor summary used in title details response."""

    id: int = Field(..., examples=[7])
    imdb_reference_id: str | None = Field(..., examples=["nm0000206"])
    name: str = Field(..., examples=["Keanu Reeves"])
    roles: list[str] = Field(..., examples=[["actor"]])


class TitleDetailsResponse(BaseModel):
    """Detailed title response."""

    id: int = Field(..., examples=[10])
    imdb_reference_id: str | None = Field(..., examples=["tt0133093"])
    title: str = Field(..., examples=["The Matrix"])
    release_year: int | None = Field(..., examples=[1999])
    media_type: str = Field(..., examples=["movie"])
    genres: list[str] = Field(..., examples=[["Action", "Sci-Fi"]])
    contributors: list[ContributorSummaryResponse]


class ContributorTitleResponse(BaseModel):
    """Title summary used in contributor details response."""

    id: int = Field(..., examples=[10])
    imdb_reference_id: str | None = Field(..., examples=["tt0133093"])
    title: str = Field(..., examples=["The Matrix"])
    release_year: int | None = Field(..., examples=[1999])
    media_type: str = Field(..., examples=["movie"])
    roles: list[str] = Field(..., examples=[["actor"]])


class ContributorDetailsResponse(BaseModel):
    """Detailed contributor response."""

    id: int = Field(..., examples=[7])
    imdb_reference_id: str | None = Field(..., examples=["nm0000206"])
    name: str = Field(..., examples=["Keanu Reeves"])
    titles: list[ContributorTitleResponse]


DEFAULT_ERROR_RESPONSES: dict[int, dict] = {
    400: {
        "model": ErrorResponse,
        "description": "Invalid request input.",
    },
    500: {
        "model": ErrorResponse,
        "description": "Internal server error.",
    },
}

