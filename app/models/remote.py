from sqlalchemy import Column, Integer, String, Float, Text
from ..database import Base

class Remote(Base):
    __tablename__ = "remotes"

    id = Column(Integer, primary_key=True, index=True)
    site_id_poi = Column(String(255), index=True, nullable=True)
    site_name = Column(String(255), index=True, nullable=False)
    notes = Column(Text, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    origin_backbone = Column(String(255), nullable=True)
    origin_bb = Column(String(255), nullable=True)
    terminating_bb = Column(String(255), nullable=True)
    link = Column(String(255), nullable=True)
    jumlah_bts = Column(Integer, nullable=True)
    bw = Column(String(255), nullable=True)
    vlan = Column(String(255), nullable=True)
