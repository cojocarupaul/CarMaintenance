from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.adapters.user import UserAdapter
from src.models.base import Base
from src.utils.exceptions import Conflict
from src.utils.validators import validate_user_body


class User(Base, UserAdapter):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(500), nullable=False)
    salt = Column(String(500))
    session = Column(String(1024))

    @classmethod
    def get_users(cls, db_session):
        results = db_session.query(cls).all()
        return cls.to_json(results)

    @classmethod
    def create_user(cls, db_session, body):
        validate_user_body(body)
        if(cls.get_user_by_email(db_session, body.get("email"))):
            raise Conflict("This email address is already used", status=409)
        user = User()
        user.to_object(body)
        db_session.add(user)
        db_session.commit()

    @classmethod
    def get_user_by_email(cls, db_session, email):
        return db_session.query(cls).filter_by(email=email).first()
