from sqlalchemy import Column, Integer, String, Table, ForeignKey
from app.database import Base

# Association Table for Role and Permission
role_permission_association = Table(
    'role_permission_association', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False) # e.g., "ticket:create"
