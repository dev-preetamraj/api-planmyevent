from pydantic import BaseModel
from typing import Any


class CustomResponseModel(BaseModel):
    success: bool
    status_code: int
    data: Any
    message: str
