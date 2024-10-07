import pytest
from database import Highscore
from modules import ActiveGames, Game, UIHighscore, sort_highscores, guess_is_valid
from sqlalchemy.orm import Session


def test_guess_is_valid():
    for zahl in range(0, 101):
        assert guess_is_valid(str(zahl)), True
    assert guess_is_valid("-1"), False
    assert guess_is_valid("101"), False
    assert guess_is_valid("e"), False


def test_save_game(db_session: Session):
    test_game = Game()
    test_game.save_game(db_session, "test_user")
    assert (db_session
            .query(Highscore)
            .where(Highscore.username == "test_user")
            .all())


@pytest.mark.parametrize('guess, msg', [
    (51, 'Zu groß'),
    (50, 'Richtig geraten'),
    (49, 'Zu klein')
])
def test_get_response_message(guess, msg):
    test_game = Game()
    test_game.number = 50
    assert test_game.get_response_message(guess)[0], msg


def test_active_games():
    test_game_list = ActiveGames()
    test_game = Game()
    test_game_list.start_game(test_game)
    assert test_game_list.get_game_by_id(test_game.id), test_game
    test_game_list.stop_game(test_game)
    assert not test_game_list.games
    assert type(test_game_list.get_game_by_id(None)), Game


def test_ui_highscore(db_session: Session):
    test_game1 = Game()
    test_game2 = Game()
    test_game3 = Game()
    db_session.add(Highscore(game_id=test_game1.id,
                             username="test_user",
                             tries=3))
    db_session.add(Highscore(game_id=test_game2.id,
                             username="test_user",
                             tries=5))
    db_session.add(Highscore(game_id=test_game3.id,
                             username="test_user",
                             tries=1))
    test_list = (db_session
                 .query(Highscore)
                 .all())
    sorted_list = sort_highscores(test_list)
    test_highscore1 = UIHighscore("test_user", 1)
    test_highscore2 = UIHighscore("test_user", 3)
    test_highscore3 = UIHighscore("test_user", 5)

    assert sort_highscores(test_list)[0], test_highscore1
    assert sort_highscores(test_list)[1], test_highscore2
    assert sort_highscores(test_list)[2], test_highscore3
