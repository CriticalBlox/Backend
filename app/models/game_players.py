from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.schemas.game import Team, TeamType


class GamePlayers(Base):
    __tablename__ = 'game_players'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey('games.id'), nullable=True)
    roblox_id: Mapped[int] = mapped_column(Integer, nullable=True)
    team: Mapped[Team] = mapped_column(TeamType)
    kill: Mapped[int] = mapped_column(Integer, default=0)
    death: Mapped[int] = mapped_column(Integer, default=0)

    game = relationship("Game", back_populates="players")
    user = relationship("User", back_populates="game_players")
