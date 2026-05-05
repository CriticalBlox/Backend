import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Enum


class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"
    superadmin = "superadmin"


UserRoleType = Enum(
    UserRole,
    name="user_role",
    native_enum=True
)


class UserBase(BaseModel):
    pseudo: str | None = None
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=24)
    role: UserRole = UserRole.user


class UserUpdate(BaseModel):
    pseudo: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: UserRole | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True
