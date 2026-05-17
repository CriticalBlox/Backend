from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.games import Game
from app.schemas.game import GameCreate, GameUpdate


def get_game(db: Session, game_id: int):
    game = db.query(Game).filter(Game.id == game_id).first()

    if game:
        return game

    raise HTTPException(status_code=404, detail="Partie introuvable")


def get_all_games(db: Session, page: int = 1, size: int = 10):
    if page < 1:
        page = 1

    offset = (page - 1) * size

    return db.query(Game).offset(offset).limit(size).all()


def create_game(db: Session, game: GameCreate):
    db_game = Game(
        map_name=game.map_name,
        winner_team=game.winner_team,
        rounds_total=game.rounds_total,
        red_score=game.red_score,
        blue_score=game.blue_score,
    )

    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


def update_game(db: Session, game_id: int, game_update: GameUpdate):
    db_game = get_game(db, game_id)

    update_data = game_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_game, key, value)

    db.commit()
    db.refresh(db_game)

    return db_game


def delete_game(db: Session, game_id: int):
    db_game = get_game(db, game_id)

    db.delete(db_game)
    db.commit()

    return {"detail": f"Partie id:{game_id} supprimée avec succès"}
