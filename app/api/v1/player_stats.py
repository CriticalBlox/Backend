from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.schemas.player_stats import PlayerStatsResponse, PlayerStatsCreate, PlayerStatsUpdate
from app.services import player_stats_service
from app.services.jwt_service import require_role
from app.services.x_api_key import require_api_key_or_admin

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.post("", response_model=PlayerStatsResponse, status_code=status.HTTP_201_CREATED)
def create_stat(stats: PlayerStatsCreate, db: Session = Depends(get_db), _auth: dict = Depends(require_api_key_or_admin)):
    return player_stats_service.create_stats_check_existing(db, stats)


@router.get("", response_model=list[PlayerStatsResponse])
def get_stat(page: int = 1, db: Session = Depends(get_db)):
    return player_stats_service.get_all_stats(db, page)


@router.get("/{stats_id}", response_model=PlayerStatsResponse)
def get_stat_by_id(stats_id: int, db: Session = Depends(get_db)):
    return player_stats_service.get_stats_by_id(db, stats_id)


@router.delete("/{stats_id}")
def delete_stat_by_id(stats_id: int, db: Session = Depends(get_db),_current_user = Depends(require_role("admin", "superadmin"))):
    return player_stats_service.delete_stats(db, stats_id)


@router.patch("/{stats_id}", response_model=PlayerStatsResponse)
def update_stat(stats_id: int, stat_update: PlayerStatsUpdate, db: Session = Depends(get_db), _auth: dict = Depends(require_api_key_or_admin)):
    return player_stats_service.update_stats(db, stats_id, stat_update)
