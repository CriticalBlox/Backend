from fastapi import FastAPI

from app.api.v1 import crud_user, player_stats, games, rounds, game_players,authentification,leaderboard
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Api Critical_Blox", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://frontend-1-jonn.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentification.router)
app.include_router(leaderboard.router)
app.include_router(crud_user.router)
app.include_router(player_stats.router)
app.include_router(games.router)
app.include_router(rounds.router)
app.include_router(game_players.router)
