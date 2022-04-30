import json
from flask import Blueprint, Response, request
from src.models.user import User
from src.utils.decorators import http_handling, session


login_bp = Blueprint('authorization', __name__, url_prefix='/')


@login_bp.route('login', methods=['POST'])
@session
@http_handling
def login(db_session):
    session_id = User.login(db_session, request.json)
    return Response(response=json.dumps({'session_id': session_id}), status=200)


@login_bp.route('logout', methods=['POST'])
@session
@http_handling
def logout(db_session):
    session_id = request.headers.get('Authorization')
    User.logout(db_session, session_id)
    return Response(response=json.dumps({'message': 'Logged out succesfully'}), status=200)
