from flask import Blueprint, request
from modules import JsonResponse, User, register_user
from sqlalchemy import Engine
from sqlalchemy.orm import Session


def create_users_blueprint(connection_pool: Engine, key: str) -> Blueprint:
    blueprint = Blueprint('users', __name__)

    @blueprint.route("/register", methods=['POST'])
    def register():
        body: dict = request.get_json()
        new_user = User(body.get('username'),
                        body.get('password'))
        (error, is_valid) = new_user.is_valid()
        if not is_valid:
            return error
        with Session(connection_pool) as session:
            return register_user(session, new_user)

    @blueprint.route("/login", methods=['POST'])
    def login():
        body: dict = request.get_json()
        user = User(body.get('username'),
                    body.get('password'))
        (error, is_valid) = user.is_valid()
        if not is_valid:
            return error
        with Session(connection_pool) as session:
            (error, token) = user.login(session, key)
            if not token:
                return error
        return JsonResponse('Logged in successfully', 200, {'token': token})

    return blueprint
