from database import Highscore
from flask import Blueprint, request
from modules import (ActiveGames, JsonResponse, get_auth_token, get_payload,
                     guess_is_valid, request_is_authorized)
from sqlalchemy import Engine
from sqlalchemy.orm import Session


def create_game_blueprint(connection_pool: Engine, key: str, games: ActiveGames) -> Blueprint:
    blueprint = Blueprint('game', __name__)

    @blueprint.route("/guess", methods=['POST'])
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
            return JsonResponse('Invalid gameId!', 401)

        current_game.tries += 1
        (response_message, active) = current_game.get_response_message(int(guess))
        if not active:
            with Session(connection_pool) as session:
                payload = get_payload(get_auth_token(request), key)
                current_game.save_game(session, payload.get('user'))
            games.stop_game(current_game)

        body = {
            'tries': current_game.tries,
            'gameId': str(current_game.id),
            'active': active
        }
        return JsonResponse(response_message, 200, body)

    @blueprint.route("/highscore")
    def get_highscore():
        with Session(connection_pool) as session:
            _ = session.query(Highscore).all()

    return blueprint
