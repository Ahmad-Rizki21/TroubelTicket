from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from .. import models, schemas, crud
from .auth import get_db, get_current_active_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/", response_model=schemas.DashboardData)
def get_dashboard_data(
    period: str = "week",  # today, week, month, year
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # Calculate date range based on period
    now = datetime.utcnow()
    if period == "today":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start_date = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "month":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == "year":
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_date = now - timedelta(days=7)  # default to week

    # Stats
    total_tickets = db.query(models.Ticket).count()
    open_tickets = db.query(models.Ticket).filter(models.Ticket.status == "Open").count()
    completed_tickets = db.query(models.Ticket).filter(models.Ticket.status == "Closed").count()
    
    # Calculate average resolution time for closed tickets
    avg_resolution_time = 0
    closed_tickets = db.query(models.Ticket).filter(
        models.Ticket.status == "Closed",
        models.Ticket.closed_at.isnot(None)
    ).all()
    
    if closed_tickets:
        total_duration = 0
        for ticket in closed_tickets:
            if ticket.created_at and ticket.closed_at:
                duration = (ticket.closed_at - ticket.created_at).total_seconds()
                total_duration += duration
        if len(closed_tickets) > 0:
            avg_resolution_time = total_duration / len(closed_tickets)
    
    # Format average resolution time as days:hours:minutes
    avg_resolution_time_str = "0"
    if avg_resolution_time > 0:
        days = int(avg_resolution_time // 86400)
        hours = int((avg_resolution_time % 86400) // 3600)
        minutes = int((avg_resolution_time % 3600) // 60)
        if days > 0:
            avg_resolution_time_str = f"{days}d {hours}h"
        elif hours > 0:
            avg_resolution_time_str = f"{hours}h {minutes}m"
        else:
            avg_resolution_time_str = f"{minutes}m"
    
    # Total remotes count
    total_remotes = db.query(models.Remote).count()
    
    stats = schemas.DashboardStats(
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        completed_tickets=completed_tickets,
        avg_resolution_time=avg_resolution_time_str,
        total_remotes=total_remotes
    )
    
    # Status distribution
    status_counts = db.query(
        models.Ticket.status,
        func.count(models.Ticket.id)
    ).group_by(models.Ticket.status).all()
    
    status_distribution = [
        schemas.TicketStatusData(status=status, count=count) 
        for status, count in status_counts
    ]
    
    # Priority distribution
    priority_counts = db.query(
        models.Ticket.priority,
        func.count(models.Ticket.id)
    ).group_by(models.Ticket.priority).all()
    
    priority_distribution = [
        schemas.TicketPriorityData(priority=priority, count=count) 
        for priority, count in priority_counts
    ]
    
    # Recent tickets (most recent 5)
    recent_tickets_query = db.query(models.Ticket).order_by(models.Ticket.created_at.desc()).limit(5).all()
    recent_tickets = [
        schemas.RecentTicket(
            id=ticket.id,
            ticket_code=ticket.ticket_code,
            title=ticket.title,
            status=ticket.status,
            priority=ticket.priority,
            created_at=ticket.created_at.isoformat() if ticket.created_at else ""
        ) for ticket in recent_tickets_query
    ]
    
    # Top categories (grouping by title or description for now)
    # In a real application, you might have a category field
    # For now, we'll use a simplified approach
    category_counts = db.query(
        models.Ticket.title,
        func.count(models.Ticket.id)
    ).group_by(models.Ticket.title).order_by(func.count(models.Ticket.id).desc()).limit(4).all()
    
    total_ticket_count = sum(count for _, count in category_counts) if category_counts else 1
    top_categories = []
    for title, count in category_counts:
        category_name = title[:30] + "..." if len(title) > 30 else title  # Truncate long titles
        percentage = round((count / total_ticket_count) * 100) if total_ticket_count > 0 else 0
        top_categories.append(
            schemas.TicketCategoryData(
                name=category_name,
                count=count,
                percentage=percentage
            )
        )
    
    return schemas.DashboardData(
        stats=stats,
        status_distribution=status_distribution,
        priority_distribution=priority_distribution,
        recent_tickets=recent_tickets,
        top_categories=top_categories
    )