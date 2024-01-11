from datetime import datetime, timedelta

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from accounts.models import User
from planMyEvent.conf import settings
from planMyEvent.logger import logger


class JwtManager:
    def __init__(self):
        pass

    @staticmethod
    def create_access_token(user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES),
            "iat": datetime.utcnow(),
        }

        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return access_token

    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow()
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRY_DAYS),
            "iat": datetime.utcnow(),
        }

        refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return refresh_token

    @classmethod
    def refresh_access_token(cls, refresh_token: str, db: Session) -> str | None:
        try:
            payload = jwt.decode(
                refresh_token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = payload.get("user_id")
            user = db.query(User).filter_by(id=user_id).first()

            if not user:
                return None

            access_token = cls.create_access_token(user_id)
            return access_token

        except JWTError as jwt_err:
            logger.error(jwt_err)
            return None

        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def verify_token(token: str) -> bool:
        try:
            jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
            return True
        except JWTError as jwt_err:
            logger.error(jwt_err)
            return False
        except Exception as e:
            logger.error(e)
            return False
