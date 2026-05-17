from typing import Optional

from pydantic import BaseModel


class PlayerStatsBase(BaseModel):
    roblox_id: int
    pseudo: str


class PlayerStatsCreate(PlayerStatsBase):
    kills: int
    deaths: int
    match_played: int
    win_total: int
    lose_total: int


class PlayerStatsUpdate(BaseModel):
    pseudo: Optional[str] = None
    kills: Optional[int] = None
    deaths: Optional[int] = None
    match_played: Optional[int] = None
    win_total: Optional[int] = None
    lose_total: Optional[int] = None


class PlayerStatsResponse(PlayerStatsBase):
    id: int
    kills: int
    deaths: int
    match_played: int
    win_total: int
    lose_total: int

    class Config:
        from_attributes = True
