from datetime import datetime

from sqlalchemy import DateTime, func, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PlayerStats(Base):
    __tablename__ = 'player_stats'

    id: Mapped[int] = mapped_column(primary_key=True)
    pseudo: Mapped[str] = mapped_column(String(50), nullable=False)
    roblox_id: Mapped[int] = mapped_column(Integer, unique=True)
    kills: Mapped[int] = mapped_column(Integer, default=0)
    deaths: Mapped[int] = mapped_column(Integer, default=0)
    match_played: Mapped[int] = mapped_column(Integer, default=0)
    win_total: Mapped[int] = mapped_column(Integer, default=0)
    lose_total: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
