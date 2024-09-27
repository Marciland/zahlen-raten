from uuid import UUID as py_UUID
from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import TEXT, UUID

from .base import Base


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
