from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud, models
from .auth import get_db, has_permission

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
)

@router.post("/", response_model=schemas.Permission, status_code=status.HTTP_201_CREATED)
def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("permission:create"))):
    db_permission = crud.get_permission_by_name(db, name=permission.name)
    if db_permission:
        raise HTTPException(status_code=400, detail="Permission with this name already exists")
    return crud.create_permission(db=db, permission=permission)

@router.get("/", response_model=List[schemas.Permission])
def read_permissions(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("permission:read"))
):
    permissions = crud.get_permissions(db, skip=skip, limit=limit)
    return permissions

@router.get("/{permission_id}", response_model=schemas.Permission)
def read_permission(
    permission_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("permission:read"))
):
    db_permission = crud.get_permission(db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

@router.put("/{permission_id}", response_model=schemas.Permission)
def update_permission(
    permission_id: int, permission: schemas.PermissionUpdate, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("permission:update"))
):
    db_permission = crud.update_permission(db=db, permission_id=permission_id, permission_in=permission)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("permission:delete"))
):
    db_permission = crud.delete_permission(db=db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)