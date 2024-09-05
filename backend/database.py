from uuid import UUID as py_UUID, uuid4
from sqlalchemy import create_engine
from sqlalchemy.types import UUID, TEXT
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from sqlalchemy.engine import Engine


class Base(DeclarativeBase, MappedAsDataclass):
    '''Cannot use DeclarativeBase directly.'''


class Player(Base):
    __tablename__ = "player"
    player_id: Mapped[py_UUID] = mapped_column(type_=UUID,
                                               default_factory=uuid4,
                                               primary_key=True,
                                               nullable=False)

    username: Mapped[str] = mapped_column(type_=TEXT,
                                          default=None,
                                          primary_key=False,
                                          nullable=False)

    password: Mapped[str] = mapped_column(type_=TEXT,
                                          default=None,
                                          primary_key=False,
                                          nullable=False)


def create_connection_pool(db: str) -> Engine:
    connection_string = f'sqlite:///database/{db}'
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    return engine
