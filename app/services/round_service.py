from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.rounds import Round
from app.schemas.round import RoundCreate, RoundUpdate


def get_round(db: Session, round_id: int):
    round_ = db.query(Round).filter(Round.id == round_id).first()

    if round_:
        return round_

    raise HTTPException(status_code=404, detail="Manche introuvable")


def get_rounds_by_game(db: Session, game_id: int):
    return db.query(Round).filter(Round.game_id == game_id).all()


def get_round_by_number(db: Session, game_id: int, round_number: int, ):
    return db.query(Round).filter(Round.game_id == game_id, Round.round_number == round_number).first()


def create_round(db: Session, round_: RoundCreate):
    existing_round = get_round_by_number(db, round_.game_id, round_.round_number)

    if existing_round:
        raise HTTPException(
            status_code=400,
            detail="Cette manche existe déjà pour cette partie"
        )

    db_round = Round(
        game_id=round_.game_id,
        round_number=round_.round_number,
        winner_team=round_.winner_team,
    )

    db.add(db_round)
    db.commit()
    db.refresh(db_round)

    return db_round


def update_round(db: Session, round_id: int, round_update: RoundUpdate):
    db_round = get_round(db, round_id)

    update_data = round_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_round, key, value)

    db.commit()
    db.refresh(db_round)

    return db_round


def delete_round(db: Session, round_id: int):
    db_round = get_round(db, round_id)

    db.delete(db_round)
    db.commit()

    return {"detail": f"Manche id:{round_id} supprimée avec succès"}
