from random import SystemRandom
from uuid import UUID, uuid4

from database import Highscore
from sqlalchemy.orm import Session

from .response import JsonResponse

randomizer = SystemRandom()


def guess_is_valid(guess: str) -> tuple[JsonResponse, bool]:
    if not guess.isdigit():
        return JsonResponse('Not a number!', 400), False
    guess = int(guess)
    if 100 < guess or guess < 0:
        return JsonResponse('Invalid number!', 400), False
    return None, True


def sort_highscores(scores: list[Highscore]) -> list[Highscore]:
    pass


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

    def get_response_message(self, guess: int) -> tuple[str, bool]:
        if guess > self.number:
            return 'Zu groß', True
        if guess < self.number:
            return 'Zu klein', True
        if guess == self.number:
            return 'Richtig geraten', False


class ActiveGames:
    games: list[Game]

    def __init__(self) -> None:
        self.games = []

    def get_game_by_id(self, game_id: UUID | None) -> Game | None:
        if not game_id:
            new_game = Game()
            self.start_game(new_game)
            return new_game
        for game in self.games:
            if game.id == UUID(str(game_id)):
                return game

    def start_game(self, game: Game):
        self.games.append(game)

    def stop_game(self, game: Game):
        self.games.remove(game)
