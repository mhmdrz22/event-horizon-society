from pydantic import BaseModel, constr, conint
from typing import Optional
from datetime import datetime # date and time are part of datetime
from .user import User # For embedding organizer information

class EventBase(BaseModel):
    title: constr(min_length=1, max_length=255)
    description: Optional[str] = None
    event_datetime: datetime # Combined date and time
    location: constr(min_length=1, max_length=255)
    capacity: conint(gt=0) # Capacity must be greater than 0

class EventCreate(EventBase):
    pass # registered_count will be default 0 from model, organizer_id from auth

class EventUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=255)] = None
    description: Optional[str] = None
    event_datetime: Optional[datetime] = None
    location: Optional[constr(min_length=1, max_length=255)] = None
    capacity: Optional[conint(gt=0)] = None

class EventResponse(EventBase): # Renamed from Event to EventResponse for clarity if Event is used for EventRegistration's event field
    id: int
    organizer_id: int
    registered_count: conint(ge=0)
    created_at: datetime
    updated_at: datetime
    organizer: Optional[User] = None # Embed organizer details
    is_registered: bool = False # To indicate if the current user is registered

    # Pydantic V2 compatibility
    model_config = {"from_attributes": True}

# Schemas for EventRegistration
class EventRegistrationBase(BaseModel):
    # user_id will be implicit from authenticated user for creation
    # event_id will be path parameter for registration
    pass # No common fields needed for base if user_id and event_id are handled by context

class EventRegistrationCreate(BaseModel):
    """
    Schema for creating an event registration. No fields are required since
    event_id is provided via path parameter and user_id is obtained from the authenticated user.
    """
    pass


class EventRegistrationResponse(BaseModel): # Renamed from EventRegistration to EventRegistrationResponse
    id: int
    user_id: int
    event_id: int
    registered_at: datetime
    user: Optional[User] = None # Optional: Embed user details
    # To avoid circular dependency if Event schema has list[EventRegistrationResponse], use a simpler EventBase here.
    event: Optional[EventBase] = None

    # Pydantic V2 compatibility
    model_config = {"from_attributes": True}
