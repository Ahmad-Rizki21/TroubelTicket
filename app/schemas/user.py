# app/schemas/user.py
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .role import Role

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role_id: int

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None

class User(UserBase):
    id: int
    role_id: int
    created_at: datetime
    role: Role
    model_config = ConfigDict(from_attributes=True)
