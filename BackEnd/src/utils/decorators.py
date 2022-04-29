import functools
import logging
import json
from flask import Response
from database_management import get_database_session

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
