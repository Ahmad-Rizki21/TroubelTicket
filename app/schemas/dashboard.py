from pydantic import BaseModel
from typing import List

class DashboardStats(BaseModel):
    total_tickets: int
    open_tickets: int
    completed_tickets: int
    avg_resolution_time: str
    total_remotes: int

class TicketStatusData(BaseModel):
    status: str
    count: int

class TicketPriorityData(BaseModel):
    priority: str
    count: int

class RecentTicket(BaseModel):
    id: int
    ticket_code: str
    title: str
    status: str
    priority: str
    created_at: str

class TicketCategoryData(BaseModel):
    name: str
    count: int
    percentage: int

class DashboardData(BaseModel):
    stats: DashboardStats
    status_distribution: List[TicketStatusData]
    priority_distribution: List[TicketPriorityData]
    recent_tickets: List[RecentTicket]
    top_categories: List[TicketCategoryData]