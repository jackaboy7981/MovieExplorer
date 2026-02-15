"""Application-level custom exceptions."""


class AppException(Exception):
    """Base exception for application errors."""

    def __init__(self, message: str, status_code: int, error_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class TitleNotFound(AppException):
    """Raised when a movie cannot be found by id."""

    def __init__(self, movie_id: int) -> None:
        super().__init__(
            message=f"Movie with ID {movie_id} not found",
            status_code=404,
            error_code=1001,
        )


class ContributorNotFound(AppException):
    """Raised when a contributor cannot be found by id."""

    def __init__(self, contributor_id: int) -> None:
        super().__init__(
            message=f"Contributor with ID {contributor_id} not found",
            status_code=404,
            error_code=1002,
        )


class InvalidInputError(AppException):
    """Raised when client input is invalid."""

    def __init__(self, field_name: str) -> None:
        super().__init__(
            message=f"Invalid input: {field_name} is invalid",
            status_code=400,
            error_code=1000,
        )


class DataProviderError(AppException):
    """Raised for generic data provider failures."""

    def __init__(self) -> None:
        super().__init__(
            message="Internal Server Error",
            status_code=500,
            error_code=501,
        )


class ConnectionPoolNotInitializedError(AppException):
    """Raised when database connection pool has not been initialized."""

    def __init__(self) -> None:
        super().__init__(
            message="Internal Server Error",
            status_code=500,
            error_code=502,
        )
