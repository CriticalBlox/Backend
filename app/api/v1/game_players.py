from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.schemas.game_players import GamePlayersCreate, GamePlayersResponse, GamePlayersUpdate
from app.services import game_player_service
from app.services.jwt_service import require_role
from app.services.x_api_key import require_api_key_or_admin

router = APIRouter(prefix="/game-players", tags=["Game Players"])


@router.post("", response_model=GamePlayersResponse, status_code=status.HTTP_201_CREATED)
def create_game_player(game_player: GamePlayersCreate, db: Session = Depends(get_db)):
    return game_player_service.create_game_player(db, game_player)


@router.get("/game/{game_id}", response_model=list[GamePlayersResponse])
def get_players_by_game(game_id: int, db: Session = Depends(get_db), _auth: dict = Depends(require_api_key_or_admin)):
    return game_player_service.get_players_by_game(db, game_id)


@router.get("/{game_player_id}", response_model=GamePlayersResponse)
def get_game_player_by_id(game_player_id: int, db: Session = Depends(get_db)):
    return game_player_service.get_game_player(db, game_player_id)


@router.delete("/{game_player_id}")
def delete_game_player(game_player_id: int, db: Session = Depends(get_db),_current_user = Depends(require_role("admin", "superadmin"))):
    return game_player_service.delete_game_player(db, game_player_id)


@router.patch("/{game_player_id}", response_model=GamePlayersResponse)
def update_game_player(game_player_id: int, game_player_update: GamePlayersUpdate, db: Session = Depends(get_db), _auth: dict = Depends(require_api_key_or_admin)):
    return game_player_service.update_game_player(db, game_player_id, game_player_update)
