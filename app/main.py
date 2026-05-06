from fastapi import FastAPI

from app.api.v1 import crud_user, player_stats

app = FastAPI(title="My API", version="1.0")

app.include_router(crud_user.router)
app.include_router(player_stats.router)
