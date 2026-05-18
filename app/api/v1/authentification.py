from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.schemas.user import UserLogin, UserResponse
from app.services import auth_service, user_service
from app.services.jwt_service import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db), ):
    return user_service.get_user(db, current_user["user_id"])


@router.post("/login")
def login(user_login: UserLogin, response: Response, db: Session = Depends(get_db)):
    return auth_service.login_user(db, user_login, response)


@router.post("/logout")
def logout(response: Response):
    return auth_service.logout_user(response)
