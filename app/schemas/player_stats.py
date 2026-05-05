from pydantic import BaseModel


class PlayerStatsBase(BaseModel):
    roblox_id: int | None = None


class PlayerStatsUpdate(BaseModel):
    kill: int | None = None
    death: int | None = None
    match_played: int | None = None
    win_total: int | None = None
    lose_total: int | None = None


class PlayerStatsResponse(PlayerStatsBase):
    id: int
    kill: int
    death: int
    match_played: int
    win_total: int
    lose_total: int

    class Config:
        from_attributes = True
