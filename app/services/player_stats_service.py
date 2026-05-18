from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import player_stats
from app.models.player_stats import PlayerStats
from app.schemas.player_stats import PlayerStatsCreate, PlayerStatsUpdate


def get_stats_by_id(db: Session, stat_id: int):
    stat = db.query(PlayerStats).filter(PlayerStats.id == stat_id).first()
    if stat is not None:
        return stat

    raise HTTPException(
        status_code=400,
        detail="Aucune stats"
    )


def get_stats_by_roblox_id(db: Session, roblox_id: int):
    return db.query(PlayerStats).filter(PlayerStats.roblox_id == roblox_id).first()


def get_all_stats(db: Session, page: int = 1, size: int = 10):
    if page < 1:
        page = 1

    offset = (page - 1) * size

    return db.query(PlayerStats).offset(offset).limit(size).all()


def create_stats(db: Session, stats: PlayerStatsCreate):
    db_user = player_stats.PlayerStats(
        roblox_id=stats.roblox_id,
        pseudo=stats.pseudo,
        kills=stats.kills,
        deaths=stats.deaths,
        match_played=stats.match_played,
        win_total=stats.win_total,
        lose_total=stats.lose_total,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_stats_check_existing(db: Session, stats: PlayerStatsCreate):
    existing_stats = get_stats_by_roblox_id(db, stats.roblox_id)

    if existing_stats:
        raise HTTPException(
            status_code=400,
            detail="Stats joueur déjà existante"
        )

    return create_stats(db, stats)


def delete_stats(db: Session, stat_id: int):
    stat = get_stats_by_id(db, stat_id)

    if not stat:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable"
        )

    db.delete(stat)
    db.commit()

    return {"detail": f"Stats id: {stat.id} (roblox_id: {stat.roblox_id}) a été supprimé avec succès"}


def update_stats(db: Session, stat_id: int, stats_update: PlayerStatsUpdate):
    db_stats = get_stats_by_id(db, stat_id)

    if not db_stats:
        return None

    update_data = stats_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_stats, key, value)

    db.commit()
    db.refresh(db_stats)

    return db_stats

def get_leaderboard(db: Session, page: int = 1, size: int = 10):
    if page < 1:
        page = 1

    offset = (page - 1) * size

    players = (
        db.query(PlayerStats)
        .order_by(
            PlayerStats.kills.desc(),
            PlayerStats.deaths.asc(),
        )
        .offset(offset)
        .limit(size)
        .all()
    )

    return [
        {
            "pseudo": player.pseudo,
            "kills": player.kills,
            "deaths": player.deaths,
            "win_total": player.win_total,
        }
        for player in players
    ]
