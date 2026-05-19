from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.games import Game
from app.schemas.game import GameCreate, GameUpdate


def get_game(db: Session, game_id: int):
    game = db.query(Game).filter(Game.id == game_id).first()

    if game:
        return game

    raise HTTPException(status_code=404, detail="Partie introuvable")


def get_all_games(db: Session, page: int = 1, size: int = 5):
    if page < 1:
        page = 1

    if size < 1:
        size = 5

    offset = (page - 1) * size

    return db.query(Game).order_by(Game.id.desc()).offset(offset).limit(size).all()


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

    for player in db_game.players:
        db.delete(player)

    for round_ in db_game.rounds:
        db.delete(round_)

    db.delete(db_game)
    db.commit()

    return {"detail": f"Partie id:{game_id} supprimée avec succès"}
