import uuid

from passlib.context import CryptContext
from sqlalchemy import Column, ForeignKey, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from planMyTrip.database import Base
from planMyTrip.utils.models import TimestampMixin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(100), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(50))  # User/Admin/Organizer
    profile_image = Column(String(500))
    phone_number = Column(String(15))
    date_of_birth = Column(DateTime)
    address = Column(String(255))

    def __init__(
        self,
        email: str,
        username: str,
        password: str,
        phone_number: str,
        first_name: str | None = None,
        last_name: str | None = None,
        role: str = "customer",
        profile_image: str = "",
        date_of_birth: DateTime | None = None,
        address: str = None,
    ):
        self.email = email
        self.username = username
        self.password = pwd_context.hash(password)
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.profile_image = profile_image
        self.date_of_birth = date_of_birth
        self.address = address

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    def as_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if not callable(value) and not key.startswith("_")
        }


class PaymentHistory(Base, TimestampMixin):
    __tablename__ = "payment_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    payment_amount = Column(Float)
    payment_date = Column(DateTime)
    payment_status = Column(String)  # Successful/Failed/Pending

    user = relationship("User")


class PasswordResetToken(Base, TimestampMixin):
    __tablename__ = "password_reset_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    token = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    expiration_time = Column(DateTime)

    user = relationship("User")


class AccountVerificationToken(Base, TimestampMixin):
    __tablename__ = "account_verification_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    token = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    expiration_time = Column(DateTime)

    user = relationship("User")
