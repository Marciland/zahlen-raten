from uuid import UUID, uuid4
from random import SystemRandom
from sqlalchemy.orm import Session
from database import Highscore

randomizer = SystemRandom()


class Game:
    id: UUID
    number: int
    tries: int

    def __init__(self) -> None:
        self.id = uuid4()
        self.number = randomizer.randint(0, 100)
        self.tries = 0

    def save_game(self, session: Session, current_user: str):
        session.add(Highscore(game_id=self.id,
                              username=current_user,
                              tries=self.tries))
        session.commit()
        # remove from list


class ActiveGames:
    games: list[Game]

    def __init__(self) -> None:
        self.games = []

    def get_game_by_id(self, game_id: UUID) -> Game | None:
        for game in self.games:
            if game.id == game_id:
                return game

    def start_game(self, game: Game):
        self.games.append(game)
