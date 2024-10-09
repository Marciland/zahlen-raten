from dataclasses import dataclass
from datetime import datetime, timedelta

from argon2 import PasswordHasher
from database import Player
from jwt import encode
from sqlalchemy.orm import Session

from .response import JsonResponse


@dataclass
class User:
    username: str
    password: str

    def is_valid(self) -> tuple[JsonResponse | None, bool]:
        if not self.username:
            return JsonResponse('missing username', 500), False
        if not self.password:
            return JsonResponse('missing password', 500), False
        return None, True

    def login(self, session: Session, key: str) -> tuple[JsonResponse, str]:
        player = session.query(Player).where(Player.username ==
                                             self.username).all()
        if player and PasswordHasher().verify(player[0].password, self.password):
            payload = {
                'exp': int((datetime.now() + timedelta(minutes=15)).timestamp()),
                'user': player[0].username
            }
            return None, encode(payload=payload, key=key, algorithm='HS256')
        return JsonResponse('Unable to login with these credentials', 404), None


def player_exists(session: Session, username: str) -> bool:
    return bool(session
                .query(Player)
                .where(Player.username == username)
                .all())


def register_user(session: Session, user: User) -> tuple[dict, int]:
    if player_exists(session, user.username):
        return JsonResponse('User already exists!', 409)
    hashed_password = PasswordHasher().hash(user.password)
    session.add(Player(username=user.username, password=hashed_password))
    session.commit()
    return JsonResponse('User created successfully!', 201)
