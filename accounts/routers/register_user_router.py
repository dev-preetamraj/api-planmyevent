from enum import Enum

from fastapi import APIRouter, status, Depends
from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field
from sqlalchemy.orm import Session

from accounts.models import User
from accounts.repository import AccountsRepository
from planMyEvent.database import get_db
from planMyEvent.logger import logger
from planMyEvent.utils.custom_exceptions import InternalServerError
from planMyEvent.utils.custom_response import CustomResponse
from planMyEvent.utils.custom_response_schema import CustomResponseModel

router = APIRouter(prefix="/register")

repository = AccountsRepository()


class RoleEnum(Enum):
    customer = "customer"
    organizer = "organizer"
    admin = "admin"


class RegisterUserRequestModel(BaseModel):
    email: EmailStr
    username: str
    phone_number: str
    password: str = Field(min_length=8)
    confirm_password: str
    role: RoleEnum = RoleEnum.customer

    @field_validator("password")
    @classmethod
    def password_length(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value

    @model_validator(mode="after")
    def passwords_match(self):
        password = self.password
        confirm_password = self.confirm_password

        if (
            password is not None
            and confirm_password is not None
            and password != confirm_password
        ):
            raise ValueError("Passwords did not matched")
        return self

    @field_validator("email")
    @classmethod
    def validate_unique_email(cls, value):
        try:
            user = repository.get_user_by_email(value)
        except Exception as e:
            logger.error(e)
            raise InternalServerError

        if user:
            raise ValueError("Email already exists")
        return value

    @field_validator("username")
    @classmethod
    def validate_unique_username(cls, value):
        try:
            user = repository.get_user_by_username(value)
        except Exception as e:
            logger.error(e)
            raise InternalServerError

        if user:
            raise ValueError("Username already exists")
        return value


class RegisterUserResponseModel(CustomResponseModel):
    data: str


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponseModel
)
async def register_user_route(
    data: RegisterUserRequestModel, db: Session = Depends(get_db)
):
    try:
        role = data.role.value
        data = data.model_dump()
        data.pop("confirm_password")
        data.pop("role")
        user = User(**data, role=role)
        db.add(user)
        db.commit()
        return CustomResponse(message="User registered successfully", data=str(user.id))
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise InternalServerError
