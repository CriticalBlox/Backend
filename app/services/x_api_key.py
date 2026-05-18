import os

from dotenv import load_dotenv
from fastapi import Header, HTTPException, status, Request

from app.services.jwt_service import get_current_user

load_dotenv()

API_KEY = os.getenv("API_KEY")


def verify_api_key(x_api_key: str = Header()):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )


def require_api_key_or_admin(request: Request,
    x_api_key: str | None = Header(
    default=None,
    alias="X-API-Key",
    )):
    
    if x_api_key == API_KEY:
        return {
            "type": "api_key"
        }

    try:
        current_user = get_current_user(request)

        if current_user["role"] in ["admin", "superadmin"]:
            return current_user

    except HTTPException:
        pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Accès refusé",
    )
