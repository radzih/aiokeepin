class KeepinException(BaseException):
    pass


class KeepinStatusError(KeepinException):
    status_code: int

    def __init__(self, *args: object) -> None:
        self.status_code = args[-2]
