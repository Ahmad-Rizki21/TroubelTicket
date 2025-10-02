from pydantic import BaseModel, ConfigDict
from typing import Optional

class RemoteBase(BaseModel):
    site_id_poi: Optional[str] = None
    site_name: str
    notes: Optional[str] = None
    latitude: float
    longitude: float
    origin_backbone: Optional[str] = None
    origin_bb: Optional[str] = None
    terminating_bb: Optional[str] = None
    link: Optional[str] = None
    jumlah_bts: Optional[int] = None
    bw: Optional[str] = None
    vlan: Optional[str] = None

class RemoteCreate(RemoteBase):
    pass

class RemoteUpdate(RemoteBase):
    site_id_poi: Optional[str] = None
    site_name: Optional[str] = None
    notes: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    origin_backbone: Optional[str] = None
    origin_bb: Optional[str] = None
    terminating_bb: Optional[str] = None
    link: Optional[str] = None
    jumlah_bts: Optional[int] = None
    bw: Optional[str] = None
    vlan: Optional[str] = None

class Remote(RemoteBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
