# app/schemas/ticket.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, timedelta
from .user import User
from .ticket_action import TicketAction

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str
    category: Optional[str] = None
    reporter_name: str
    reporter_contact: Optional[str] = None
    
class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    reporter_contact: Optional[str] = None
    assignee_id: Optional[int] = None
    summary_problem: Optional[str] = None
    summary_action: Optional[str] = None

class Ticket(TicketBase):
    id: int
    ticket_code: str
    status: str
    reporter_contact: Optional[str] = None
    assignee_id: Optional[int] = None
    created_at: datetime
    closed_at: Optional[datetime] = None
    downtime: Optional[timedelta] = None

    assignee: Optional[User] = None
    
    # DISempurnakan: Menampilkan daftar semua riwayat aksi untuk tiket ini
    actions: List[TicketAction] = []
    
    model_config = ConfigDict(from_attributes=True)
