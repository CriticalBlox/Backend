from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.schemas.game import Team, TeamType


class GamePlayers(Base):
    __tablename__ = 'game_players'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey('games.id'), nullable=False)
    roblox_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pseudo: Mapped[str] = mapped_column(String(50), nullable=False)
    team: Mapped[Team] = mapped_column(TeamType)
    kills: Mapped[int] = mapped_column(Integer, default=0)
    deaths: Mapped[int] = mapped_column(Integer, default=0)

    game = relationship("Game", back_populates="players")
    user = relationship("User", back_populates="game_players")
