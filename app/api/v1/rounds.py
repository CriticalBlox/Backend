from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.schemas.round import RoundCreate, RoundResponse, RoundUpdate
from app.services import round_service
from app.services.jwt_service import require_role
from app.services.x_api_key import require_api_key_or_admin

router = APIRouter(prefix="/rounds", tags=["Rounds"])


@router.post("", response_model=RoundResponse, status_code=status.HTTP_201_CREATED)
def create_round(round_: RoundCreate, db: Session = Depends(get_db), _auth: dict = Depends(require_api_key_or_admin)):
    return round_service.create_round(db, round_)


@router.get("/game/{game_id}", response_model=list[RoundResponse])
def get_rounds_by_game(game_id: int, db: Session = Depends(get_db)):
    return round_service.get_rounds_by_game(db, game_id)


@router.get("/{round_id}", response_model=RoundResponse)
def get_round_by_id(round_id: int, db: Session = Depends(get_db)):
    return round_service.get_round(db, round_id)


@router.delete("/{round_id}")
def delete_round(round_id: int, db: Session = Depends(get_db),_current_user = Depends(require_role("admin", "superadmin"))):
    return round_service.delete_round(db, round_id)


@router.patch("/{round_id}", response_model=RoundResponse)
def update_round(round_id: int, round_update: RoundUpdate, db: Session = Depends(get_db), _auth: dict = Depends(require_api_key_or_admin)):
    return round_service.update_round(db, round_id, round_update)
