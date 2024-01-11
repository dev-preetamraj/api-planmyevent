import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from planMyTrip.database import Base
from planMyTrip.utils.models import TimestampMixin


class Event(Base, TimestampMixin):
    __tablename__ = 'events'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    title = Column(String(100))
    description = Column(String(500))
    date = Column(DateTime)
    location = Column(String(255))
    organizer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    category = Column(String(100))
    capacity = Column(Integer)
    price = Column(Float)

    organizer = relationship("User")


class RSVP(Base, TimestampMixin):
    __tablename__ = 'rsvps'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'))
    response = Column(String(50))  # Attending/Not Attending/Maybe Attending
