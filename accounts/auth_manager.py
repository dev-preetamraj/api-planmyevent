from typing import Annotated, Optional

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError

from accounts.models import User
from planMyEvent.conf import settings
from planMyEvent.database import session
from planMyEvent.logger import logger
from planMyEvent.utils.custom_exceptions import InternalServerError


class CustomAuthentication:
    def __init__(self):
        pass

    def __call__(self, request: Request) -> Optional[str]:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header not provided",
            )
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header",
            )
        access_token = auth_header.split(" ")[-1]
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
            )
        return access_token


manager = CustomAuthentication()


async def get_current_user(access_token: Annotated[str, Depends(manager)]):
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
            )
        user = session.query(User).filter_by(id=user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return user.as_dict()

    except JWTError as jwe:
        logger.error(jwe)
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

    except Exception as e:
        logger.error(e)
        raise InternalServerError


user_dependency = Annotated[dict, Depends(get_current_user)]
