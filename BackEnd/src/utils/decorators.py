import functools
import logging
import json
from flask import Response, request
from database_management import get_database_session
from src.models.user import User
from src.utils.exceptions import HTTPException

logger = logging.getLogger(__name__)


def session(func):
    @functools.wraps(func)
    def warpper(*args, **kwargs):
        db_session = get_database_session()
        kwargs["db_session"] = db_session
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            db_session.close()
    return warpper


def http_handling(func):
    @functools.wraps(func)
    def warpper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            status = getattr(e, "status", 500)
            return Response(status=status, response=json.dumps({"error": e.args[0]}))
    return warpper


def is_authorized(func):
    @functools.wraps(func)
    def wrapper(*args, **kargs):
        db_session = kargs['db_session']
        session_id = request.headers.get('Authorization')
        if not session_id:
            raise HTTPException("You must provide a session id", status=401)
        user = User.get_user_by_session(session_id)
        if not user:
            raise HTTPException(
                "You are not allowed to acces this", status=401)
        kargs['user'] = user
        return func(*args, **kargs)
    return wrapper
