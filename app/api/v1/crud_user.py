from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services import user_service
from app.services.jwt_service import get_optional_current_user, get_current_user, require_role
from app.services.x_api_key import verify_api_key, require_api_key_or_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db),
                current_user: dict | None = Depends(get_optional_current_user)):
    return user_service.create_user_with_role_check(db, user, current_user)


@router.post("/admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_admin(user: UserCreate, db: Session = Depends(get_db), _api_key: str = Depends(verify_api_key)):
    return user_service.create_user_check_existing(db, user)


@router.get("", response_model=list[UserResponse])
def get_users(page: int = 1, db: Session = Depends(get_db), _current_user=Depends(get_current_user)):
    return user_service.get_all_users(db, page)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), _current_user=Depends(get_current_user)):
    return user_service.get_user(db, user_id)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db),
                _current_user=Depends(require_role("admin", "superadmin"))):
    return user_service.delete_user(db, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db),
                _auth: dict = Depends(require_api_key_or_admin)):
    return user_service.update_user(db, user_id, user)
