from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from accounts.auth_manager import user_dependency
from events.models import Event
from events.schema import EventResponseModel, EventsResponseModel
from planMyEvent.database import get_db
from planMyEvent.logger import logger
from planMyEvent.utils.custom_exceptions import InternalServerError
from planMyEvent.utils.custom_response import CustomResponse

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=EventsResponseModel)
async def get_events(user: user_dependency, db: Session = Depends(get_db)):
    try:
        events = db.query(Event).filter_by(organizer_id=user["id"]).all()
        return CustomResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            message="Successfully retrieved all events",
            data=events,
        )
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise InternalServerError


@router.get(
    "/{event_id}", status_code=status.HTTP_200_OK, response_model=EventResponseModel
)
async def get_event_by_id_route(
    event_id: str, user: user_dependency, db: Session = Depends(get_db)
):
    try:
        event = db.query(Event).filter_by(id=event_id, organizer_id=user["id"]).first()
        db.commit()

        if event is None:
            return CustomResponse(
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Event not found",
                data=None,
            ).json_response()

        return CustomResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            message="Event fetched successfully",
            data=event,
        )
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise InternalServerError
