from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.adapters.user import UserAdapter
from src.models.base import Base
from src.utils.exceptions import Conflict, HTTPException
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
    def get_user_by_id(cls, db_session, user_id):
        return db_session.query(cls).filter_by(id=user_id).first()

    @classmethod
    def get_user_by_email(cls, db_session, email):
        return db_session.query(cls).filter_by(email=email).first()

    @classmethod
    def get_user_by_session(cls, db_session, session_id):
        return db_session.query(cls).filter_by(session=session_id).first()

    @classmethod
    def login(cls, db_session, body):
        user = cls.get_user_by_email(db_session, body.get('email'))
        if not user:
            raise HTTPException(
                "The email or the password is incorrect", status=400)

        password, _ = cls.generate_password(
            body.get('password'), user.salt.encode('utf-8'))
        if password != user.password:
            raise HTTPException(
                "The email or the password is incorrect", status=400)

        session_id = cls.generate_session()
        user.session = session_id
        db_session.commit()
        return session_id

    @classmethod
    def logout(cls, db_session, session_id):
        user = cls.get_user_by_session(db_session, session_id)
        if not user:
            raise HTTPException("User not found", status=400)

        user.session = None
        db_session.commit()
