import json
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from argon2 import PasswordHasher
from database import Player, create_connection_pool
from flask import Flask, Response, request
from flask_cors import CORS
from game import ActiveGames, Game
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from sqlalchemy.orm import Session
from werkzeug.exceptions import HTTPException

games = ActiveGames()


def main():
    key = str(uuid4())
    # key = "test"
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
        return json.dumps({'detail': 'User created successfully!'}), 200

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

    @ app.route("/guess", methods=['POST'])
    def guessing_game():
        try:
            token = request.headers.get('Authorization').split(' ')[1]
        except Exception:
            return Response('Missing token!', status=401)
        try:
            payload: dict = jwt.decode(jwt=token,
                                       key=key,
                                       algorithms=['HS256'])
        except (InvalidSignatureError, ExpiredSignatureError):
            return json.dumps({'detail': 'Invalid token!'}), 401

        body: dict = request.get_json()
        game_id = body.get('gameId')
        guess: str = body.get('guess')

        if not guess.isdigit():
            return json.dumps({'detail': 'Not a number!'}), 400

        guess = int(guess)
        if 100 < guess or guess < 0:
            return json.dumps({'detail': 'Invalid number!'}), 400

        if not games.get_game_by_id(game_id):
            new_game = Game()
            game_id = new_game.id
            games.start_game(new_game)

        current_game = games.get_game_by_id(game_id)

        if guess > current_game.number:
            response_message = 'Zu groß'
        if guess < current_game.number:
            response_message = 'Zu klein'
        if guess == current_game.number:
            response_message = 'Richtig geraten'
            with Session(highscore_connection_pool) as session:
                current_game.save_game(session, payload.get('user'))
        current_game.tries += 1
        return json.dumps({'detail': response_message, 'gameId': current_game.id}), 200

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
