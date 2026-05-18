import hashlib

import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import users
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate, UserRole


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if user is not None:
        return user

    raise HTTPException(
        status_code=400,
        detail="Aucun utilisateur"
    )


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session, page: int = 1, size: int = 10):
    if page < 1:
        page = 1

    offset = (page - 1) * size

    return db.query(User).offset(offset).limit(size).all()


def create_user(db: Session, user: UserCreate):
    password_hash = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    db_user = users.User(
        pseudo=user.pseudo or "",
        email=user.email,
        password=password_hash,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_user_check_existing(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email déjà enregistré"
        )

    return create_user(db, user)


def verify_pwd(db: Session, email: str, password: str):
    user = db.query(users.User).filter(users.User.email == email).first()

    if not user:
        return False

    return bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8")
    )


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable"
        )

    db.delete(user)
    db.commit()

    return {"detail": f"Utilisateur: {user.pseudo} (id: {user.id}) a été supprimé avec succès"}


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)

    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "password":
            raw_password = update_data.pop("password")

            pre_hash = hashlib.sha256(raw_password.encode("utf-8")).hexdigest()
            hashed_password = bcrypt.hashpw(
                pre_hash.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            update_data["password"] = hashed_password
        else:
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def create_user_with_role_check(db: Session, user: UserCreate, current_user: dict | None):
    if not current_user or current_user["role"] != UserRole.superadmin:
        user.role = UserRole.user

    return create_user_check_existing(db, user)
