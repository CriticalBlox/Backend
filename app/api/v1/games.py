from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.schemas.game import GameCreate, GameResponse, GameUpdate
from app.services import game_service

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    return game_service.create_game(db, game)


@router.get("", response_model=list[GameResponse])
def get_games(page: int = 1, db: Session = Depends(get_db)):
    return game_service.get_all_games(db, page)


@router.get("/{game_id}", response_model=GameResponse)
def get_game_by_id(game_id: int, db: Session = Depends(get_db)):
    return game_service.get_game(db, game_id)


@router.delete("/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db)):
    return game_service.delete_game(db, game_id)


@router.patch("/{game_id}", response_model=GameResponse)
def update_game(game_id: int, game_update: GameUpdate, db: Session = Depends(get_db)):
    return game_service.update_game(db, game_id, game_update)
