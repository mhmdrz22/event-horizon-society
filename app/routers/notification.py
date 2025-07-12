from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user
from app.db.session import get_db
from app.services.notification_service import notification_service

router = APIRouter()

@router.get("/", response_model=List[schemas.Notification])
def read_notifications(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve notifications for the current user.
    """
    notifications = notification_service.get_multi_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return notifications

@router.put("/{notification_id}", response_model=schemas.Notification)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Mark a specific notification as read.
    """
    notification = notification_service.get(db, id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    notification = notification_service.update(
        db, db_obj=notification, obj_in={"is_read": True}
    )
    return notification

@router.put("/mark-all-as-read", status_code=status.HTTP_204_NO_CONTENT)
def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
) -> None:
    """
    Mark all unread notifications for the current user as read.
    """
    notification_service.mark_all_as_read(db, user_id=current_user.id)
    return None
