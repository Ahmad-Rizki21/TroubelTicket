from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from .permission import role_permission_association

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    permissions = relationship(
        "Permission",
        secondary=role_permission_association,
        backref="roles"
    )
