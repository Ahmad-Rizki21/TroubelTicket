# app/routers/ticket_actions.py

from fastapi import APIRouter, Depends, UploadFile, File, Form
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
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    image_url = None
    if image:
        # Pastikan direktori upload ada
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # Buat nama file yang unik
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Simpan file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        # Buat path URL
        image_url = f"/static/uploads/{unique_filename}"

    # Buat objek skema untuk fungsi CRUD
    action_schema = schemas.TicketActionCreate(
        action_description=action_description,
        action_image_url=image_url
    )
    
    return crud.create_ticket_action(db=db, action=action_schema, ticket_id=ticket_id, user_id=current_user.id)


@router.get("/", response_model=List[schemas.TicketAction])
def read_actions_for_ticket(
    ticket_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    actions = crud.get_actions_for_ticket(db=db, ticket_id=ticket_id)
    return actions