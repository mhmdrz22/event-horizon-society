from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user
from app.database import get_db
from app.services.event_service import event_service

router = APIRouter()

@router.get("/", response_model=List[schemas.EventResponse])
def read_events(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve events.
    """
    events = event_service.get_multi(db, skip=skip, limit=limit)
    return events

@router.post("/", response_model=schemas.EventResponse)
def create_event(
    *,
    db: Session = Depends(get_db),
    event_in: schemas.EventCreate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Create new event.
    """
    if current_user.role != models.user.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions to create an event")
    event = event_service.create(db=db, obj_in=event_in, organizer_id=current_user.id)
    return event

from app.dependencies import get_current_user_optional
from app.services.event_registration_service import event_registration_service

@router.get("/{event_id}", response_model=schemas.EventResponse)
def read_event_by_id(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user_optional),
) -> Any:
    """
    Get event by ID.
    """
    event = event_service.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    is_registered = False
    if current_user:
        registration = event_registration_service.get_by_user_and_event(
            db, user_id=current_user.id, event_id=event.id
        )
        if registration:
            is_registered = True

    # Manually construct the response to include the is_registered flag
    event_data = schemas.EventResponse.model_validate(event)
    event_data.is_registered = is_registered

    return event_data

@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(
    *,
    db: Session = Depends(get_db),
    event_id: int,
    event_in: schemas.EventUpdate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Update an event.
    """
    event = event_service.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id and current_user.role != models.user.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    event = event_service.update(db=db, db_obj=event, obj_in=event_in)
    return event

@router.delete("/{event_id}", response_model=schemas.EventResponse)
def delete_event(
    *,
    db: Session = Depends(get_db),
    event_id: int,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Delete an event.
    """
    event = event_service.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id and current_user.role != models.user.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    event = event_service.remove(db=db, id=event_id)
    return event
