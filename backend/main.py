import json
from uuid import uuid4

from flask import Flask, Response, request
from flask_cors import CORS
from modules import (ActiveGames, Highscore, Player, User,
                     create_connection_pool, get_auth_token, get_payload,
                     guess_is_valid, register_user, request_is_authorized,
                     token_is_valid)
from sqlalchemy.orm import Session

games = ActiveGames()


def main():
    key = str(uuid4())
    app = Flask(__name__)
    CORS(app)

    player_connection_pool = create_connection_pool(
        'sqlite:///database/player.db')
    highscore_connection_pool = create_connection_pool(
        'sqlite:///database/highscore.db')

    @app.route("/validate", methods=['GET'])
    def validate_token():
        (_, is_valid) = token_is_valid(request.args.get('token'), key)
        return Response(json.dumps({'valid': is_valid}), 200)

    @app.route("/register", methods=['POST'])
    def register():
        body: dict = request.get_json()
        new_user = User(body.get('username'),
                        body.get('password'))
        (error, is_valid) = new_user.is_valid()
        if not is_valid:
            return error
        with Session(player_connection_pool) as session:
            return register_user(session, new_user)

    @ app.route("/login", methods=['POST'])
    def login():
        body: dict = request.get_json()
        user: User = User(body.get('username'),
                          body.get('password'))
        (error, is_valid) = user.is_valid()
        if not is_valid:
            return error
        with Session(player_connection_pool) as session:
            (error, token) = user.login(session, key)
            if not token:
                return error
        return {'token': token}

    @ app.route("/guess", methods=['POST'])
    def guessing_game():
        (error, authorized) = request_is_authorized(request, key)
        if not authorized:
            return error

        body: dict = request.get_json()

        guess: str = body.get('guess')
        (error, is_valid) = guess_is_valid(guess)
        if not is_valid:
            return error

        game_id = body.get('gameId')
        current_game = games.get_game_by_id(game_id)
        if not current_game:
            return json.dumps({'detail': 'Invalid gameId!'}), 401

        current_game.tries += 1
        (response_message, active) = current_game.get_response_message(int(guess))
        if not active:
            with Session(highscore_connection_pool) as session:
                payload = get_payload(get_auth_token(request), key)
                current_game.save_game(session, payload.get('user'))
            games.stop_game(current_game)

        return Response(json.dumps({'detail': response_message,
                                    'tries': current_game.tries,
                                    'gameId': str(current_game.id),
                                    'active': active}),
                        200)

    @ app.route("/highscore")
    def get_highscore():
        # returns the scores + names
        return ""

    @ app.route("/debug")
    def debugging():
        with Session(player_connection_pool) as session:
            all_players = session.query(Player).all()
        with Session(highscore_connection_pool) as session:
            all_highscores = session.query(Highscore).all()
        return {'players': all_players, 'highscores': all_highscores}

    app.run()


if __name__ == '__main__':
    main()
