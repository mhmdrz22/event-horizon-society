from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.session import get_db
from app.services.event_service import event_service
from app.services.event_registration_service import event_registration_service
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.EventResponse)
def create_event(
    *,
    db: Session = Depends(get_db),
    event_in: schemas.EventCreate,
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Create a new event (requires admin or association admin role).
    """
    if not current_user.is_superuser and current_user.role != models.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    event = event_service.create(db, obj_in=event_in, organizer_id=current_user.id)
    return event

@router.get("/", response_model=List[schemas.EventResponse])
def get_events(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Retrieve events.
    """
    events = event_service.get_multi(db, skip=skip, limit=limit)
    event_objs = []
    for event in events:
        registration = event_registration_service.get_by_user_and_event(
            db, user_id=current_user.id, event_id=event.id
        )
        event_obj = schemas.EventResponse.model_validate(event)
        event_obj.is_registered = bool(registration)
        event_objs.append(event_obj)
    return event_objs

@router.get("/{event_id}", response_model=schemas.EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Retrieve a specific event by ID.
    """
    event = event_service.get(db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    registration = event_registration_service.get_by_user_and_event(
        db, user_id=current_user.id, event_id=event.id
    )
    event_obj = schemas.EventResponse.model_validate(event)
    event_obj.is_registered = bool(registration)
    return event_obj

@router.post(
    "/{event_id}/register",
    response_model=schemas.EventRegistrationResponse,
    summary="Register for an event",
    description="Allows a user to register for an event if there is available capacity."
)
def register_for_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    event = event_service.get(db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    registration = event_registration_service.create_with_event_id(
        db, obj_in=schemas.EventRegistrationCreate(), user_id=current_user.id, event_id=event_id
    )
    return registration

@router.delete("/{event_id}/register", response_model=schemas.EventRegistrationResponse)
def unregister_from_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Unregister from an event.
    """
    registration = event_registration_service.remove_registration(db, user_id=current_user.id, event_id=event_id)
    return registration
