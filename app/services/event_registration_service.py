from sqlalchemy.orm import Session
from .base import ServiceBase
from app.models.event_registration import EventRegistration
from app.schemas.event import EventRegistrationCreate

from typing import List, Optional

class EventRegistrationService(ServiceBase[EventRegistration, EventRegistrationCreate, None]): # No Update
    def create_with_event_id(self, db: Session, *, obj_in: EventRegistrationCreate, user_id: int, event_id: int) -> EventRegistration:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id, event_id=event_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user_and_event(
        self, db: Session, *, user_id: int, event_id: int
    ) -> Optional[EventRegistration]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id, self.model.event_id == event_id)
            .first()
        )

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[EventRegistration]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

event_registration_service = EventRegistrationService(EventRegistration)
