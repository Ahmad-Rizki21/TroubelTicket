# app/schemas/ticket_action.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from .user import User

class TicketActionBase(BaseModel):
    action_description: str
    action_image_url: Optional[str] = None

class TicketActionCreate(TicketActionBase):
    pass

class TicketAction(TicketActionBase):
    id: int
    ticket_id: int
    user_id: int
    created_at: datetime
    user: User
    model_config = ConfigDict(from_attributes=True)
