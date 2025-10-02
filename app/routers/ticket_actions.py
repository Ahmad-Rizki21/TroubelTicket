# app/routers/ticket_actions.py

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import uuid
import os

from .. import schemas, models, crud
from .auth import get_current_active_user, get_db

router = APIRouter(
    prefix="/tickets/{ticket_id}/actions",
    tags=["Ticket Actions"]
)

UPLOAD_DIR = "static/uploads"

@router.post("/", response_model=schemas.TicketAction)
async def create_action_for_ticket(
    ticket_id: int,
    action_description: str = Form(...),
    image: Optional[UploadFile] = File(None),
    assignee_id: Optional[int] = Form(None),  # To re-assign the ticket
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # Handle file upload
    image_url = None
    if image:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = os.path.join(UPLOAD_DIR, unique_filename).replace("\\", "/")

    # If assignee_id is provided, update the main ticket's assignee
    if assignee_id is not None:
        ticket_update_schema = schemas.TicketUpdate(assignee_id=assignee_id)
        crud.update_ticket(db=db, ticket_id=ticket_id, ticket=ticket_update_schema)

    # Create the ticket action
    action_schema = schemas.TicketActionCreate(
        action_description=action_description,
        action_image_url=image_url
    )
    
    return crud.create_ticket_action(db=db, action=action_schema, ticket_id=ticket_id, user_id=current_user.id)


@router.put("/{action_id}/", response_model=schemas.TicketAction)
def update_action(
    ticket_id: int,
    action_id: int,
    action_description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    assignee_id: Optional[int] = Form(None), # To re-assign the ticket
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_action = crud.get_ticket_action(db, action_id=action_id)
    if not db_action:
        raise HTTPException(status_code=404, detail="Action not found")

    # Check if the action belongs to the ticket
    if db_action.ticket_id != ticket_id:
        raise HTTPException(status_code=400, detail="Action does not belong to this ticket")

    update_data = schemas.TicketActionUpdate()

    if action_description is not None:
        update_data.action_description = action_description

    if image:
        # If there was an old image, delete it
        if db_action.action_image_url:
            # Construct absolute path to check for existence and delete
            old_image_path = db_action.action_image_url.lstrip('/')
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        # Save the new image
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        # Store path relative to the static directory
        update_data.action_image_url = os.path.join(UPLOAD_DIR, unique_filename).replace("\\", "/")

    updated_action = crud.update_ticket_action(db=db, action_id=action_id, action_in=update_data)
    return updated_action


@router.get("/", response_model=List[schemas.TicketAction])
def read_actions_for_ticket(
    ticket_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    actions = crud.get_actions_for_ticket(db=db, ticket_id=ticket_id)
    return actions