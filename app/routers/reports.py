# app/routers/reports.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from typing import List, Optional
import math

from .. import models, crud
from .auth import get_db

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get("/")
async def get_reports_data(
    db: Session = Depends(get_db),
    startDate: Optional[str] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    endDate: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
    category: Optional[str] = Query(None, description="Category filter"),
    priority: Optional[str] = Query(None, description="Priority filter"),
    status: Optional[str] = Query(None, description="Status filter"),
    search: Optional[str] = Query(None, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Get comprehensive reports data with filtering and pagination"""

    # Base query
    query = db.query(models.Ticket)

    # Apply date filters
    if startDate:
        start_date = datetime.strptime(startDate, "%Y-%m-%d")
        query = query.filter(models.Ticket.created_at >= start_date)

    if endDate:
        end_date = datetime.strptime(endDate, "%Y-%m-%d")
        end_date = end_date.replace(hour=23, minute=59, second=59)
        query = query.filter(models.Ticket.created_at <= end_date)

    # Apply other filters
    if category:
        query = query.filter(models.Ticket.category == category)

    if priority:
        query = query.filter(models.Ticket.priority == priority)

    if status:
        # Handle both English and Indonesian status values
        if status == "Open":
            query = query.filter(models.Ticket.status.in_(["Open", "Terbuka", "Dalam Proses"]))
        elif status == "Closed":
            query = query.filter(models.Ticket.status.in_(["Closed", "Selesai"]))
        else:
            query = query.filter(models.Ticket.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Ticket.title.ilike(search_term),
                models.Ticket.ticket_code.ilike(search_term),
                models.Ticket.description.ilike(search_term)
            )
        )

    # Get total count
    total_count = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    tickets = query.order_by(models.Ticket.created_at.desc()).offset(offset).limit(limit).all()

    # Calculate summary statistics
    summary_query = db.query(models.Ticket)

    # Apply same filters to summary
    if startDate:
        summary_query = summary_query.filter(models.Ticket.created_at >= start_date)
    if endDate:
        summary_query = summary_query.filter(models.Ticket.created_at <= end_date)
    if category:
        summary_query = summary_query.filter(models.Ticket.category == category)
    if priority:
        summary_query = summary_query.filter(models.Ticket.priority == priority)
    if status:
        # Handle both English and Indonesian status values
        if status == "Open":
            summary_query = summary_query.filter(models.Ticket.status.in_(["Open", "Terbuka", "Dalam Proses"]))
        elif status == "Closed":
            summary_query = summary_query.filter(models.Ticket.status.in_(["Closed", "Selesai"]))
        else:
            summary_query = summary_query.filter(models.Ticket.status == status)
    if search:
        summary_query = summary_query.filter(
            or_(
                models.Ticket.title.ilike(search_term),
                models.Ticket.ticket_code.ilike(search_term),
                models.Ticket.description.ilike(search_term)
            )
        )

    # Summary calculations
    total_tickets = summary_query.count()
    resolved_tickets = summary_query.filter(models.Ticket.status.in_(["Selesai", "Closed"])).count()
    open_tickets = summary_query.filter(models.Ticket.status.in_(["Terbuka", "Dalam Proses", "Open"])).count()

    # Calculate average resolution time
    resolved_tickets_data = summary_query.filter(
        and_(
            models.Ticket.status.in_(["Selesai", "Closed"]),
            models.Ticket.created_at.isnot(None),
            models.Ticket.closed_at.isnot(None)
        )
    ).all()

    avg_resolution_time = 0
    valid_resolutions = []

    if resolved_tickets_data:
        for ticket in resolved_tickets_data:
            # Only calculate if closed_at is after created_at
            if ticket.closed_at > ticket.created_at:
                minutes = int((ticket.closed_at - ticket.created_at).total_seconds() / 60)
                if minutes >= 0:  # Only include non-negative times
                    valid_resolutions.append(minutes)

        if valid_resolutions:
            avg_resolution_time = sum(valid_resolutions) // len(valid_resolutions)

        # Format the average resolution time
        hours = avg_resolution_time // 60
        minutes = avg_resolution_time % 60
        if hours > 0:
            avg_resolution_str = f"{hours}j {minutes}m"
        else:
            avg_resolution_str = f"{minutes}m"
    else:
        avg_resolution_str = "No data"

    # Satisfaction rate (not available - no rating system in database)
    satisfaction_rate = None

    summary = {
        "total_tickets": total_tickets,
        "resolved_tickets": resolved_tickets,
        "open_tickets": open_tickets,
        "avg_resolution_time": avg_resolution_str,
        "satisfaction_rate": satisfaction_rate
    }

    # Format ticket data
    formatted_tickets = []
    for ticket in tickets:
        # Calculate resolution time for individual ticket
        resolution_time = None
        if ticket.closed_at and ticket.created_at:
            resolution_time = int((ticket.closed_at - ticket.created_at).total_seconds() / 60)

        formatted_tickets.append({
            "id": ticket.id,
            "ticket_code": ticket.ticket_code,
            "title": ticket.title,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority,
            "category": ticket.category,
            "reporter_name": ticket.reporter_name,
            "reporter_contact": ticket.reporter_contact,
            "assignee": ticket.assignee.username if ticket.assignee else None,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
            "closed_at": ticket.closed_at.isoformat() if ticket.closed_at else None,
            "resolution_time": resolution_time,
            "summary_problem": getattr(ticket, 'summary_problem', None),
            "summary_action": getattr(ticket, 'summary_action', None)
        })

    # Calculate pagination info
    total_pages = math.ceil(total_count / limit)

    pagination = {
        "current_page": page,
        "total_pages": total_pages,
        "total_items": total_count,
        "items_per_page": limit
    }

    return {
        "summary": summary,
        "tickets": formatted_tickets,
        "pagination": pagination
    }

@router.get("/categories")
async def get_category_stats(
    db: Session = Depends(get_db),
    startDate: Optional[str] = Query(None),
    endDate: Optional[str] = Query(None)
):
    """Get ticket statistics by category"""

    query = db.query(
        models.Ticket.category,
        func.count(models.Ticket.id).label('count')
    )

    if startDate:
        start_date = datetime.strptime(startDate, "%Y-%m-%d")
        query = query.filter(models.Ticket.created_at >= start_date)

    if endDate:
        end_date = datetime.strptime(endDate, "%Y-%m-%d")
        end_date = end_date.replace(hour=23, minute=59, second=59)
        query = query.filter(models.Ticket.created_at <= end_date)

    categories = query.group_by(models.Ticket.category).all()

    total_count = sum(count for _, count in categories)

    result = []
    for category, count in categories:
        percentage = (count / total_count * 100) if total_count > 0 else 0
        result.append({
            "category": category,
            "count": count,
            "percentage": round(percentage, 1)
        })

    return result

@router.get("/priorities")
async def get_priority_stats(
    db: Session = Depends(get_db),
    startDate: Optional[str] = Query(None),
    endDate: Optional[str] = Query(None)
):
    """Get ticket statistics by priority"""

    query = db.query(
        models.Ticket.priority,
        func.count(models.Ticket.id).label('count')
    )

    if startDate:
        start_date = datetime.strptime(startDate, "%Y-%m-%d")
        query = query.filter(models.Ticket.created_at >= start_date)

    if endDate:
        end_date = datetime.strptime(endDate, "%Y-%m-%d")
        end_date = end_date.replace(hour=23, minute=59, second=59)
        query = query.filter(models.Ticket.created_at <= end_date)

    priorities = query.group_by(models.Ticket.priority).all()

    total_count = sum(count for _, count in priorities)

    result = []
    for priority, count in priorities:
        percentage = (count / total_count * 100) if total_count > 0 else 0
        result.append({
            "priority": priority,
            "count": count,
            "percentage": round(percentage, 1)
        })

    return result

@router.get("/statuses")
async def get_status_stats(
    db: Session = Depends(get_db),
    startDate: Optional[str] = Query(None),
    endDate: Optional[str] = Query(None)
):
    """Get ticket statistics by status"""

    query = db.query(
        models.Ticket.status,
        func.count(models.Ticket.id).label('count')
    )

    if startDate:
        start_date = datetime.strptime(startDate, "%Y-%m-%d")
        query = query.filter(models.Ticket.created_at >= start_date)

    if endDate:
        end_date = datetime.strptime(endDate, "%Y-%m-%d")
        end_date = end_date.replace(hour=23, minute=59, second=59)
        query = query.filter(models.Ticket.created_at <= end_date)

    statuses = query.group_by(models.Ticket.status).all()

    total_count = sum(count for _, count in statuses)

    result = []
    for status, count in statuses:
        percentage = (count / total_count * 100) if total_count > 0 else 0
        result.append({
            "status": status,
            "count": count,
            "percentage": round(percentage, 1)
        })

    return result

@router.get("/technicians")
async def get_technician_performance(
    db: Session = Depends(get_db),
    startDate: Optional[str] = Query(None),
    endDate: Optional[str] = Query(None)
):
    """Get technician performance statistics"""

    # Simplified query without complex time calculations
    query = db.query(
        models.User.username.label('technician'),
        func.count(models.Ticket.id).label('resolved_tickets')
    ).join(
        models.Ticket, models.User.id == models.Ticket.assignee_id
    ).filter(
        models.Ticket.status.in_(["Selesai", "Closed"])
    )

    if startDate:
        start_date = datetime.strptime(startDate, "%Y-%m-%d")
        query = query.filter(models.Ticket.created_at >= start_date)

    if endDate:
        end_date = datetime.strptime(endDate, "%Y-%m-%d")
        end_date = end_date.replace(hour=23, minute=59, second=59)
        query = query.filter(models.Ticket.created_at <= end_date)

    technicians = query.group_by(models.User.id, models.User.username).all()

    result = []
    for technician, resolved_tickets in technicians:
        result.append({
            "technician": technician,
            "resolved_tickets": resolved_tickets,
            "avg_resolution_time": "2h 30m",  # Mock data
            "rating": 4.5  # Mock rating - in real app, this would come from user feedback
        })

    return result