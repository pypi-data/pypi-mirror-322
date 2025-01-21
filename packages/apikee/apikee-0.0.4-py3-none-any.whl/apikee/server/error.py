class ApiError(Exception):
    def __init__(self, message: str, status: int, details: str):
        super().__init__(message)
        self.status = status
        self.details = details


def handle_error(error: Exception):
    if hasattr(error, "response"):
        response = error.response
        raise ApiError(
            response.json().get("error", "Unknown Error"),
            response.status_code,
            response.text
        )
    elif hasattr(error, "request"):
        raise ApiError("No response from server", 0, str(error))
    else:
        raise ApiError("Unexpected Error", 0, str(error))
