from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .base import Base
from .highscore import Highscore
from .player import Player


def create_connection_pool(connection_string: str) -> Engine:
    engine = create_engine(connection_string)
    tables = []
    if 'player' in connection_string:
        tables.append(Player.__table__)
    if 'score' in connection_string:
        tables.append(Highscore.__table__)
    Base.metadata.create_all(engine, tables=tables)
    return engine
