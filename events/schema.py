from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from planMyEvent.utils.custom_response_schema import CustomResponseModel


class EventBase(BaseModel):
    title: str
    description: str
    date: datetime
    location: str
    category: str
    capacity: int
    price: float


class EventResponseData(EventBase):
    id: UUID
    organizer_id: UUID
    created_at: datetime
    updated_at: datetime


class EventRequestModel(EventBase):
    pass


class EventResponseModel(CustomResponseModel):
    data: EventResponseData


class EventsResponseModel(CustomResponseModel):
    data: List[EventResponseData]
