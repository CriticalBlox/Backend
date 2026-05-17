from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.game_players import GamePlayers
from app.schemas.game_players import GamePlayersCreate, GamePlayersUpdate


def get_game_player(db: Session, game_player_id: int):
    game_player = db.query(GamePlayers).filter(GamePlayers.id == game_player_id).first()

    if game_player:
        return game_player

    raise HTTPException(status_code=404, detail="Joueur de partie introuvable")


def get_players_by_game(db: Session, game_id: int):
    return db.query(GamePlayers).filter(GamePlayers.game_id == game_id).all()


def get_game_player_by_roblox_and_game(db: Session, roblox_id: int, game_id: int, ):
    return db.query(GamePlayers).filter(GamePlayers.roblox_id == roblox_id, GamePlayers.game_id == game_id).first()


def create_game_player(db: Session, game_player: GamePlayersCreate):
    if game_player.roblox_id is not None:
        existing_player = get_game_player_by_roblox_and_game(db, game_player.roblox_id, game_player.game_id)

        if existing_player:
            raise HTTPException(
                status_code=400,
                detail="Ce joueur existe déjà dans cette partie"
            )

    db_game_player = GamePlayers(
        user_id=game_player.user_id,
        game_id=game_player.game_id,
        roblox_id=game_player.roblox_id,
        pseudo=game_player.pseudo,
        team=game_player.team,
        kills=game_player.kills,
        deaths=game_player.deaths,
    )

    db.add(db_game_player)
    db.commit()
    db.refresh(db_game_player)

    return db_game_player


def update_game_player(db: Session, game_player_id: int, game_player_update: GamePlayersUpdate, ):
    db_game_player = get_game_player(db, game_player_id)

    update_data = game_player_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_game_player, key, value)

    db.commit()
    db.refresh(db_game_player)

    return db_game_player


def delete_game_player(db: Session, game_player_id: int):
    db_game_player = get_game_player(db, game_player_id)

    db.delete(db_game_player)
    db.commit()

    return {"detail": f"Joueur de partie id:{game_player_id} supprimé avec succès"}
