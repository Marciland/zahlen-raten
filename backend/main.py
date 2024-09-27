from uuid import uuid4

from database import Highscore, Player, create_connection_pool
from flask import Flask, request
from flask_cors import CORS
from modules import ActiveGames, JsonResponse, token_is_valid
from router import create_game_blueprint, create_users_blueprint
from sqlalchemy.orm import Session


def main():
    key = str(uuid4())
    app = Flask(__name__)
    CORS(app)

    games = ActiveGames()

    player_connection_pool = create_connection_pool(
        'sqlite:///database/player.db')
    highscore_connection_pool = create_connection_pool(
        'sqlite:///database/highscore.db')

    app.register_blueprint(create_users_blueprint(player_connection_pool,
                                                  key),
                           url_prefix='/users')

    app.register_blueprint(create_game_blueprint(highscore_connection_pool,
                                                 key,
                                                 games),
                           url_prefix='/game')

    @app.route("/validate", methods=['GET'])
    def validate_token():
        (_, is_valid) = token_is_valid(request.args.get('token'), key)
        return JsonResponse('Token is valid', 200, {'valid': is_valid})

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
