class KeepinException(BaseException):
    """Base exception for aiokeepin."""
    pass


class KeepinStatusError(KeepinException):
    """Exception raised for non 2xx status codes."""
    status_code: int

    def __init__(self, *args: object) -> None:
        self.status_code = args[0]


class InvalidAPIKeyError(KeepinStatusError):
    """Exception raised for invalid API key."""
    pass