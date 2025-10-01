# app/schemas/role.py
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from .permission import Permission

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None

class Role(RoleBase):
    id: int
    created_at: Optional[str] = None
    permissions: List[Permission] = []
    model_config = ConfigDict(from_attributes=True)
