class KeepinException(BaseException):
    """Base exception for aiokeepin."""

    pass


class KeepinStatusError(KeepinException):
    """Exception raised for non 2xx status codes."""

    status_code: int
    response: str  # str because 404 response is not JSON

    def __init__(self, *args: object) -> None:
        self.status_code = args[0]
        self.response = args[1]


class InvalidAPIKeyError(KeepinStatusError):
    """Exception raised for invalid API key."""

    pass


class ValidationError(KeepinException):
    """Exception raised for invalid data."""

    pass


class NotFoundError(KeepinStatusError):
    """Exception raised for not found resources."""

    pass


class InternalServerError(KeepinStatusError):
    """Exception raised for internal server error."""

    pass
