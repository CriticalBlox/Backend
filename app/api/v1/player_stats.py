from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.schemas.player_stats import PlayerStatsResponse, PlayerStatsCreate, PlayerStatsUpdate
from app.services import player_stats_service

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.post("", response_model=PlayerStatsResponse, status_code=status.HTTP_201_CREATED)
def create_user(stats: PlayerStatsCreate, db: Session = Depends(get_db)):
    return player_stats_service.create_stats_check_existing(db, stats)


@router.get("", response_model=list[PlayerStatsResponse])
def get_users(page: int = 1, db: Session = Depends(get_db)):
    return player_stats_service.get_all_stats(db, page)


@router.get("/{stats_id}", response_model=PlayerStatsResponse)
def get_stat(stats_id: int, db: Session = Depends(get_db)):
    return player_stats_service.get_stats_by_id(db, stats_id)


@router.delete("/{stats_id}")
def delete_user(stats_id: int, db: Session = Depends(get_db)):
    return player_stats_service.delete_stats(db, stats_id)


@router.patch("/{stats_id}", response_model=PlayerStatsResponse)
def update_user(stats_id: int, stat_update: PlayerStatsUpdate, db: Session = Depends(get_db)):
    return player_stats_service.update_stats(db, stats_id, stat_update)
