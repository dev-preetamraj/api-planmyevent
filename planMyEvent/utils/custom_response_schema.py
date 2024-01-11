from typing import Any

from pydantic import BaseModel


class CustomResponseModel(BaseModel):
    success: bool
    status_code: int
    message: str
    data: Any
