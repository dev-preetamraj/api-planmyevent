from fastapi.exceptions import HTTPException
from typing import Any


class InternalServerError(HTTPException):
    def __init__(
            self,
            success: bool = False,
            status_code: int = 500,
            data: Any = None,
            message: str = 'Something went wrong'
    ):
        self.success = success
        self.status_code = status_code
        self.data = data
        self.message = message
