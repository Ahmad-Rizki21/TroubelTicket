from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Interval
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_code = Column(String(20), unique=True, index=True)
    title = Column(String(255))
    description = Column(Text, nullable=True)
    status = Column(String(50), default="Open")
    priority = Column(String(50), default="Medium")
    category = Column(String(50), default="Lainnya")
    reporter_name = Column(String(100))
    reporter_contact = Column(String(100), nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    initial_image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
    summary_problem = Column(Text, nullable=True)
    summary_action = Column(Text, nullable=True)
    downtime = Column(Interval, nullable=True)
    assignee = relationship("User")
