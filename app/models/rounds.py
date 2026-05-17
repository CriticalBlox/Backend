from datetime import datetime

from sqlalchemy import DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.schemas.game import Team, TeamType


class Round(Base):
    __tablename__ = 'rounds'

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey('games.id'), nullable=False)
    round_number: Mapped[int] = mapped_column(Integer)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    winner_team: Mapped[Team | None] = mapped_column(TeamType, nullable=True)

    game = relationship("Game", back_populates="rounds")
