from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user
from app.db.session import get_db
from app.services.user_service import user_service

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Retrieve users. Only admins can do this.
    """
    if current_user.role != models.user.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = user_service.get_multi(db, skip=skip, limit=limit)
    return users

@router.put("/{user_id}/role", response_model=schemas.User)
def update_user_role(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Update a user's role. Only admins can do this.
    """
    if current_user.role != models.user.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = user_service.update(db, db_obj=user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserUpdate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Update own user.
    """
    user = user_service.update(db, db_obj=current_user, obj_in=user_in)
    return user
