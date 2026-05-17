from datetime import datetime

from sqlalchemy import DateTime, func, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.schemas.game import Team, TeamType


class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    map_name: Mapped[str] = mapped_column(String(255), nullable=False)
    rounds_total: Mapped[int] = mapped_column(Integer, default=0)
    red_score: Mapped[int] = mapped_column(Integer, default=0)
    blue_score: Mapped[int] = mapped_column(Integer, default=0)
    winner_team: Mapped[Team | None] = mapped_column(TeamType, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    rounds = relationship("Round", back_populates="game")
    players = relationship("GamePlayers", back_populates="game")
