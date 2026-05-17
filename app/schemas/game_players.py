from pydantic import BaseModel

from app.schemas.game import Team


class GamePlayersBase(BaseModel):
    user_id: int | None = None
    game_id: int
    roblox_id: int | None = None
    pseudo: str


class GamePlayersCreate(GamePlayersBase):
    team: Team
    kills: int = 0
    deaths: int = 0


class GamePlayersUpdate(BaseModel):
    team: Team | None = None
    kills: int | None = None
    deaths: int | None = None


class GamePlayersResponse(GamePlayersBase):
    id: int
    team: Team
    kills: int
    deaths: int

    class Config:
        from_attributes = True
