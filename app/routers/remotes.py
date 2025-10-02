from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud, models
from .auth import get_current_active_user, get_db

router = APIRouter(
    prefix="/remotes",
    tags=["Remotes"]
)

@router.post("/", response_model=schemas.Remote)
def create_remote(
    remote: schemas.RemoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return crud.create_remote(db=db, remote=remote)

@router.get("/", response_model=List[schemas.Remote])
def read_remotes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    remotes = crud.get_remotes(db, skip=skip, limit=limit)
    return remotes

@router.get("/{remote_id}", response_model=schemas.Remote)
def read_remote(
    remote_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_remote = crud.get_remote(db, remote_id=remote_id)
    if db_remote is None:
        raise HTTPException(status_code=404, detail="Remote not found")
    return db_remote

@router.put("/{remote_id}", response_model=schemas.Remote)
def update_remote(
    remote_id: int,
    remote: schemas.RemoteUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_remote = crud.update_remote(db, remote_id=remote_id, remote_in=remote)
    if db_remote is None:
        raise HTTPException(status_code=404, detail="Remote not found")
    return db_remote

@router.delete("/{remote_id}", response_model=schemas.Remote)
def delete_remote(
    remote_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_remote = crud.delete_remote(db, remote_id=remote_id)
    if db_remote is None:
        raise HTTPException(status_code=404, detail="Remote not found")
    return db_remote
