from typing import Optional

from pydantic import BaseModel


class PlayerStatsBase(BaseModel):
    roblox_id: int


class PlayerStatsCreate(PlayerStatsBase):
    kill: int
    death: int
    match_played: int
    win_total: int
    lose_total: int


class PlayerStatsUpdate(BaseModel):
    kill: Optional[int] = None
    death: Optional[int] = None
    match_played: Optional[int] = None
    win_total: Optional[int] = None
    lose_total: Optional[int] = None


class PlayerStatsResponse(PlayerStatsBase):
    id: int
    kill: int
    death: int
    match_played: int
    win_total: int
    lose_total: int

    class Config:
        from_attributes = True
