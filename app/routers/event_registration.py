from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user
from app.db.session import get_db
from app.services.event_registration_service import event_registration_service
from app.services.event_service import event_service

router = APIRouter()

@router.post("/events/{event_id}/register", response_model=schemas.EventRegistrationResponse)
def register_for_event(
    *,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Register current user for an event.
    """
    event = event_service.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check for existing registration
    existing_registration = event_registration_service.get_by_user_and_event(
        db, user_id=current_user.id, event_id=event_id
    )
    if existing_registration:
        raise HTTPException(status_code=400, detail="Already registered for this event")

    registration = event_registration_service.create_with_event_id(
        db=db, obj_in=schemas.EventRegistrationCreate(), user_id=current_user.id, event_id=event_id
    )
    return registration

@router.delete("/events/{event_id}/unregister", response_model=schemas.EventRegistrationResponse)
def unregister_from_event(
    *,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Unregister current user from an event.
    """
    registration = event_registration_service.get_by_user_and_event(
        db, user_id=current_user.id, event_id=event_id
    )
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    deleted_registration = event_registration_service.remove(db=db, id=registration.id)
    return deleted_registration

@router.get("/users/{user_id}/registrations", response_model=List[schemas.EventRegistrationResponse])
def read_user_registrations(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all event registrations for a specific user.
    """
    if user_id != current_user.id and current_user.role != models.user.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    registrations = event_registration_service.get_multi_by_user(
        db, user_id=user_id, skip=skip, limit=limit
    )
    return registrations
