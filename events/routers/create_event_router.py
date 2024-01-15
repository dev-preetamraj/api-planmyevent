from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from accounts.auth_manager import user_dependency
from events.models import Event
from events.schema import EventResponseModel, EventRequestModel
from planMyEvent.database import get_db
from planMyEvent.logger import logger
from planMyEvent.utils.custom_exceptions import InternalServerError
from planMyEvent.utils.custom_response import CustomResponse

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=EventResponseModel
)
async def create_event_route(
    data: EventRequestModel, user: user_dependency, db: Session = Depends(get_db)
):
    try:
        if user["role"] == "customer":
            return CustomResponse(
                success=False,
                status_code=status.HTTP_403_FORBIDDEN,
                message="Customers not have permission to create an event",
                data=None,
            ).json_response()
        event = Event(**data.model_dump(), organizer_id=user["id"])
        db.add(event)
        db.commit()
        return CustomResponse(
            success=True,
            status_code=status.HTTP_201_CREATED,
            message="Event created successfully",
            data=event,
        )
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise InternalServerError
