from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from .auth import get_db, has_permission

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.post("/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("role:create"))):
    db_role = crud.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role name already registered")
    return crud.create_role(db=db, role=role)

@router.get("/", response_model=List[schemas.Role])
def read_roles(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("role:read"))
):
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/{role_id}", response_model=schemas.Role)
def read_role(
    role_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("role:read"))
):
    db_role = crud.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.put("/{role_id}", response_model=schemas.Role)
def update_role(
    role_id: int, role: schemas.RoleUpdate, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("role:update"))
):
    db_role = crud.update_role(db=db, role_id=role_id, role_in=role)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("role:delete"))
):
    try:
        db_role = crud.delete_role(db=db, role_id=role_id, force=False)  # Secara default tidak force
        if db_role is None:
            raise HTTPException(status_code=404, detail="Role not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{role_id}/permissions/{permission_id}", response_model=schemas.Role)
def assign_permission_to_role(
    role_id: int, permission_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("permission:assign"))
):
    db_role = crud.add_permission_to_role(db=db, role_id=role_id, permission_id=permission_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role or Permission not found")
    return db_role

@router.delete("/{role_id}/permissions/{permission_id}", response_model=schemas.Role)
def remove_permission_from_role(
    role_id: int, permission_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("permission:assign"))
):
    db_role = crud.remove_permission_from_role(db=db, role_id=role_id, permission_id=permission_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role or Permission not found, or Permission not in Role")
    return db_role