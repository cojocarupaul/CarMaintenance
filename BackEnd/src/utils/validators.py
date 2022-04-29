import re
from unittest import result

from src.utils.exceptions import InvalidBody


def validate_user_body(body):
    validate_email(body["email"])
    validate_password(body["password"])


def validate_password(password):
    if not password:
        raise InvalidBody("You must provide a password", status=400)


def validate_email(email):
    regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    result = re.search(regex, email)
    if not result:
        raise InvalidBody("Email address is not valid", status=400)
