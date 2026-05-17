import enum
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Enum


class Team(str, enum.Enum):
    red = "red"
    blue = "blue"


TeamType = Enum(
    Team,
    name="winner_team",
    native_enum=True
)


class GameBase(BaseModel):
    map_name: str


class GameCreate(GameBase):
    winner_team: Team | None = None
    rounds_total: int = 0
    red_score: int = 0
    blue_score: int = 0


class GameUpdate(BaseModel):
    map_name: str | None = None
    winner_team: Team | None = None
    ended_at: datetime | None = None
    rounds_total: int | None = None
    red_score: int | None = None
    blue_score: int | None = None


class GameResponse(GameBase):
    id: int
    started_at: datetime
    ended_at: datetime | None
    rounds_total: int
    red_score: int
    blue_score: int
    winner_team: Team | None

    class Config:
        from_attributes = True
