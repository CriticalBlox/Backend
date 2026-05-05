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
    winner_team: Team


class GameUpdate(BaseModel):
    map_name: str | None = None
    winner_team: Team | None = None
    ended_at: datetime | None = None


class GameResponse(GameBase):
    id: int
    started_at: datetime
    ended_at: datetime | None
    rounds_total: int
    team_red: int
    team_blue: int
    winner_team: Team

    class Config:
        from_attributes = True
