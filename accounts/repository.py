from sqlalchemy.orm import Session

from accounts.models import User
from planMyTrip.database import session


class AccountsRepository:
    def __init__(self):
        pass

    @staticmethod
    def get_user_by_email(email: str, db: Session = session):
        try:
            user = db.query(User).filter_by(email=email).first()
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            user = None
            raise
        return user

    @staticmethod
    def get_user_by_username(username: str, db: Session = session):
        try:
            user = db.query(User).filter_by(username=username).first()
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            user = None
            raise
        return user
