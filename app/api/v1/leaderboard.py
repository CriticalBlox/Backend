from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import player_stats_service

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("/")
def get_leaderboard(page: int = 1,size: int = 10, db: Session = Depends(get_db),):
    return player_stats_service.get_leaderboard(db, page, size)
