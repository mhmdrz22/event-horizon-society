from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.session import get_db
from app.services.notification_service import notification_service
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Notification])
def get_notifications(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve notifications for the current user.
    """
    return notification_service.get_multi_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/mark-all-read", response_model=int)
def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Mark all notifications as read for the current user.
    """
    return notification_service.mark_all_as_read(db, user_id=current_user.id)

@router.delete("/read", response_model=int)
def delete_read_notifications(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Delete all read notifications for the current user.
    """
    return notification_service.delete_read_notifications(db, user_id=current_user.id)
