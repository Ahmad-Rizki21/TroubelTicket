# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud

from .auth import get_current_active_user, get_db, has_permission

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("user:create"))):
    # Cek apakah user dengan username yang sama sudah ada
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # Jika belum ada, panggil fungsi CRUD untuk membuat user
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("user:read"))
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("user:read"))

):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("user:update"))
):
    db_user = crud.update_user(db=db, user_id=user_id, user_in=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("user:delete"))
):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)