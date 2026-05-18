from fastapi import FastAPI

from app.api.v1 import crud_user, player_stats, games, rounds, game_players,authentification,leaderboard

app = FastAPI(title="My API", version="1.0")
app.include_router(authentification.router)
app.include_router(leaderboard.router)
app.include_router(crud_user.router)
app.include_router(player_stats.router)
app.include_router(games.router)
app.include_router(rounds.router)
app.include_router(game_players.router)
