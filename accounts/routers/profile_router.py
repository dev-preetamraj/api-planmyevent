import datetime
from uuid import UUID

from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr

from accounts.auth_manager import user_dependency
from planMyEvent.logger import logger
from planMyEvent.utils.custom_exceptions import InternalServerError
from planMyEvent.utils.custom_response import CustomResponse
from planMyEvent.utils.custom_response_schema import CustomResponseModel

router = APIRouter()


class ProfileResponseData(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    first_name: str | None
    last_name: str | None
    role: str
    profile_image: str
    phone_number: str | None
    date_of_birth: datetime.datetime | None
    address: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ProfileResponseModel(CustomResponseModel):
    data: ProfileResponseData


@router.get("/", status_code=status.HTTP_200_OK, response_model=ProfileResponseModel)
async def read_me_route(user: user_dependency):
    try:
        return CustomResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            data=user,
            message="Profile fetched successfully",
        )
    except Exception as e:
        logger.error(e)
        raise InternalServerError
