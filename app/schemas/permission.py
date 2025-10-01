from typing import Optional
from pydantic import BaseModel, ConfigDict

class PermissionBase(BaseModel):
    name: str

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = None

class Permission(PermissionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
