from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from argon2 import PasswordHasher
from database import Player, create_connection_pool
from flask import Flask, Response, request
from flask_cors import CORS
from sqlalchemy.orm import Session
from werkzeug.exceptions import HTTPException


def main():
    key = str(uuid4())
    app = Flask(__name__)
    CORS(app)

    player_database = 'sqlite:///database/player.db'
    highscore_database = 'sqlite:///database/highscore.db'
    player_connection_pool = create_connection_pool(player_database)
    highscore_connection_pool = create_connection_pool(highscore_database)

    @app.route("/register", methods=['POST'])
    def register():
        body: dict = request.get_json()
        username = body.get('username')
        hashed_password = PasswordHasher().hash(body.get('password'))
        with Session(player_connection_pool) as session:
            players = session \
                .query(Player) \
                .where(Player.username == username) \
                .all()
            if players:
                raise HTTPException(description="User already exists!",
                                    response=Response(status=409))
            session.add(Player(username=username, password=hashed_password))
            session.commit()
            return Response('User created successfully!', status=200)

    @ app.route("/login", methods=['POST'])
    def login():
        body: dict = request.get_json()
        username = body.get('username')
        password = body.get('password')
        with Session(player_connection_pool) as session:
            player = session \
                .query(Player) \
                .where(Player.username == username) \
                .all()
            if player and PasswordHasher().verify(player[0].password, password):
                payload = {
                    'exp': int((datetime.now() + timedelta(minutes=15)).timestamp()),
                    'user': player[0].username
                }
                token = jwt.encode(payload=payload, key=key, algorithm='HS256')
                return {'token': token}
            return Response(status=404)

    @ app.route("/save")
    def save_game():
        # saves a played game in the database
        # name + counter
        return ""

    @ app.route("/highscore")
    def get_highscore():
        # returns the scores + names
        return ""

    @ app.route("/debug")
    def debugging():
        with Session(player_connection_pool) as session:
            return session.query(Player).all()

    app.run()


if __name__ == '__main__':
    main()
