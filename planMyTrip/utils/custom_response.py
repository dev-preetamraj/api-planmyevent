from fastapi.responses import JSONResponse
from fastapi import status
from typing import Any


class CustomResponse:
    def __init__(
        self,
        message: str,
        success: bool = True,
        status_code: int = status.HTTP_200_OK,
        data: Any | None = None
    ):
        self.success = success
        self.status_code = status_code
        self.data = data
        self.message = message

    def json_response(self):
        return JSONResponse({
            'success': self.success,
            'status_code': self.status_code,
            'data': self.data,
            'message': self.message
        }, status_code=self.status_code)
