import json
from flask import Blueprint, Response, request

from database_management import get_database_session
from src.models.user import User
from src.utils.decorators import session, http_handling

user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('', methods=['GET'])
@session
@http_handling
def get_users(db_session):
    users = User.get_users(db_session)
    return Response(status=200, response=json.dumps(users))


@user_bp.route('', methods=['POST'])
@session
@http_handling
def post_users(db_session):  # register
    body = request.json
    User.create_user(db_session, body)
    return Response(status=201, response="Resource created")
