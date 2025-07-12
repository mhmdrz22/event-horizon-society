from sqlalchemy.orm import Session
from .base import ServiceBase
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate

class EventService(ServiceBase[Event, EventCreate, EventUpdate]):
    def create(self, db: Session, *, obj_in: EventCreate, organizer_id: int) -> Event:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, organizer_id=organizer_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

event_service = EventService(Event)
