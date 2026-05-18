from fastapi import HTTPException, Response
from sqlalchemy.orm import Session

from app.schemas.user import UserLogin
from app.services import user_service
from app.services.jwt_service import create_token


def login_user(db: Session, user_login: UserLogin, response: Response):
    is_pwd_valid = user_service.verify_pwd(db, user_login.email, user_login.password)

    if not is_pwd_valid:
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect",
        )

    user = user_service.get_user_by_email(db, user_login.email)

    token = create_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "role": user.role,
        }
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=3600,
        expires=3600,
        samesite="lax",
        secure=False,
    )

    return {
        "message": "Connexion réussie",
        "token": token,
        "user_id": user.id,
        "user_email": user.email,
        "role": user.role,
        "user_name": user.pseudo,
    }


def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Déconnexion réussie"}
