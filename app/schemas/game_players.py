from pydantic import BaseModel
from app.schemas.game import Team


class GamePlayersBase(BaseModel):
    user_id: int
    game_id: int | None = None
    roblox_id: int | None = None


class GamePlayersCreate(GamePlayersBase):
    team: Team


class GamePlayersUpdate(BaseModel):
    kill: int | None = None
    death: int | None = None


class GamePlayersResponse(GamePlayersBase):
    id: int
    team: Team
    kill: int
    death: int

    class Config:
        from_attributes = True
