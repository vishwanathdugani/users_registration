from __future__ import annotations
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# from app.db.models import Device

# class VerifyUserRequest(BaseModel):
#     email: EmailStr

class UserBase(BaseModel):
    username: EmailStr


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    verified: bool

    class Config:
        from_attributes = True


class VerifyUserRequest(BaseModel):
    email: EmailStr
