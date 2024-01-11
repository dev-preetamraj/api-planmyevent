from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from accounts.jwt_manager import JwtManager
from accounts.models import User
from planMyTrip.database import db_dependency
from planMyTrip.logger import logger
from planMyTrip.utils.custom_exceptions import InternalServerError
from planMyTrip.utils.custom_response import CustomResponse
from planMyTrip.utils.custom_response_schema import CustomResponseModel

router = APIRouter()
jwt_manager = JwtManager()


# Create Token
class CreateTokenRequestModel(BaseModel):
    email: EmailStr
    password: str


class CreateTokenResponseData(BaseModel):
    access_token: str
    refresh_token: str


class CreateTokenResponseModel(CustomResponseModel):
    data: CreateTokenResponseData | None


# Refresh Token
class RefreshTokenRequestModel(BaseModel):
    refresh_token: str


class RefreshTokenResponseData(BaseModel):
    access_token: str


class RefreshTokenResponseModel(CustomResponseModel):
    data: RefreshTokenResponseData | None


# Verify Token
class VerifyTokenRequestModel(BaseModel):
    access_token: str


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateTokenResponseModel,
)
async def create_token_route(
    data: CreateTokenRequestModel, db: Session = db_dependency
):
    try:
        user: User | None = db.query(User).filter_by(email=data.email).first()
        if user is None:
            return CustomResponse(
                success=False,
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                message="User not found",
            )

        if not user.verify_password(data.password):
            return CustomResponse(
                success=False,
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                message="Invalid credentials",
            )
        access_token = jwt_manager.create_access_token(str(user.id))
        refresh_token = jwt_manager.create_refresh_token(str(user.id))
        return_data = {"access_token": access_token, "refresh_token": refresh_token}

        return CustomResponse(
            success=True,
            status_code=status.HTTP_201_CREATED,
            data=return_data,
            message="Tokens generated",
        )
    except Exception as e:
        logger.error(e)
        raise InternalServerError


@router.post(
    "/refresh",
    status_code=status.HTTP_201_CREATED,
    response_model=RefreshTokenResponseModel,
)
async def refresh_token_route(
    data: RefreshTokenRequestModel, db: Session = db_dependency
):
    try:
        refresh_token = data.refresh_token
        access_token = jwt_manager.refresh_access_token(refresh_token, db)
        if access_token is None:
            return CustomResponse(
                success=False,
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                message="Refresh token is invalid or expired",
            )
        return_data = {"access_token": access_token}

        return CustomResponse(
            success=True,
            status_code=status.HTTP_201_CREATED,
            data=return_data,
            message="Access token refreshed",
        )
    except Exception as e:
        logger.error(e)
        raise InternalServerError


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_token_route(data: VerifyTokenRequestModel):
    try:
        access_token = data.access_token
        if not jwt_manager.verify_token(access_token):
            return CustomResponse(
                success=False,
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                message="Access token is invalid or expired",
            )

        return CustomResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            data=None,
            message="Access token verified",
        )
    except Exception as e:
        logger.error(e)
        raise InternalServerError
