import os
from datetime import datetime, timedelta, timezone
from typing import Any

from dotenv import load_dotenv
from fastapi import HTTPException, Request, status
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def create_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_token_from_request(request: Request) -> str:
    token = request.cookies.get("access_token")

    if not token:
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Pourriez-vous vous reconnecter ?",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    return token


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(request: Request):
    token = get_token_from_request(request)
    payload = decode_token(token)

    email = payload.get("sub")
    user_id = payload.get("user_id")
    role = payload.get("role")

    if not email or not user_id or not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "email": email,
        "user_id": user_id,
        "role": role,
    }


def get_optional_current_user(request: Request):
    try:
        return get_current_user(request)
    except HTTPException:
        return None


def require_role(*allowed_roles: str):
    def checker(request: Request):
        current_user = get_current_user(request)

        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission refusée",
            )

        return current_user

    return checker
