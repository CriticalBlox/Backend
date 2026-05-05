from datetime import datetime
from pydantic import BaseModel
from app.schemas.game import Team


class RoundBase(BaseModel):
    game_id: int
    round_number: int


class RoundCreate(RoundBase):
    winner_team: Team


class RoundUpdate(BaseModel):
    ended_at: datetime | None = None


class RoundResponse(RoundBase):
    id: int
    started_at: datetime
    ended_at: datetime | None
    winner_team: Team

    class Config:
        from_attributes = True
