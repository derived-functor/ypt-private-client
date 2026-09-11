class YPTError(Exception):
    """Base exception for all YPT API errors."""


class AuthenticationError(YPTError):
    """Raised when authentication fails (error codes 112, 113, missing_jwt)."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Authentication failed: {code}")


class APIError(YPTError):
    """Raised for general API errors."""

    def __init__(self, code: str, message: str = "") -> None:
        self.code = code
        self.message = message
        super().__init__(f"API error {code}: {message}" if message else f"API error {code}")


class ServerError(YPTError):
    """Raised on server-side errors (alert_server_error_msg)."""

    def __init__(self) -> None:
        super().__init__("Server error")
