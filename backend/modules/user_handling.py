import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from modules import Player
from flask import Response
from sqlalchemy.orm import Session
from werkzeug.exceptions import HTTPException
from jwt import encode


@dataclass
class User:
    username: str
    password: str

    def is_valid(self) -> tuple[Response, bool]:
        if not self.username:
            return False, 'missing username'
        if not self.password:
            return False, 'missing password'
        return True, 'valid'

    def login(self, session: Session, key: str) -> tuple[Response, str]:
        player = session \
            .query(Player) \
            .where(Player.username == self.username) \
            .all()
        if player and PasswordHasher().verify(player[0].password, self.password):
            payload = {
                'exp': int((datetime.now() + timedelta(minutes=15)).timestamp()),
                'user': player[0].username
            }
            return None, encode(payload=payload, key=key, algorithm='HS256')
        return Response(status=404), None


def player_exists(session: Session, username: str) -> bool:
    return bool(session
                .query(Player)
                .where(Player.username == username)
                .all())


def register_user(session: Session, user: User) -> tuple[dict, int]:
    if player_exists(session, user.username):
        raise HTTPException(description="User already exists!",
                            response=Response(status=409))
    hashed_password = PasswordHasher().hash(user.password)
    session.add(Player(username=user.username, password=hashed_password))
    session.commit()
    return json.dumps({'detail': 'User created successfully!'}), 200
