from datetime import datetime

from sqlalchemy import DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PlayerStats(Base):
    __tablename__ = 'player_stats'

    id: Mapped[int] = mapped_column(primary_key=True)
    roblox_id: Mapped[int] = mapped_column(Integer, unique=True)
    kill: Mapped[int] = mapped_column(Integer, default=0)
    death: Mapped[int] = mapped_column(Integer, default=0)
    match_played: Mapped[int] = mapped_column(Integer, default=0)
    win_total: Mapped[int] = mapped_column(Integer, default=0)
    lose_total: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
