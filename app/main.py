from fastapi import FastAPI

from app.api.v1 import crud_user

app = FastAPI(title="My API", version="1.0")


app.include_router(crud_user.router)
