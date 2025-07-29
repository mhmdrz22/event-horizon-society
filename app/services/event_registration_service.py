from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .base import ServiceBase
from app.models.event_registration import EventRegistration
from app.models.event import Event
from app.schemas.event import EventRegistrationCreate

class EventRegistrationService(ServiceBase[EventRegistration, EventRegistrationCreate, None]):
    def create_with_event_id(self, db: Session, *, obj_in: EventRegistrationCreate, user_id: int, event_id: int) -> EventRegistration:
        # بررسی وجود رویداد
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # بررسی ظرفیت
        if event.registered_count >= event.capacity:
            raise HTTPException(status_code=400, detail="Event is full")

        # بررسی ثبت‌نام تکراری
        existing_registration = self.get_by_user_and_event(db, user_id=user_id, event_id=event_id)
        if existing_registration:
            raise HTTPException(status_code=400, detail="User is already registered for this event")

        # ایجاد ثبت‌نام
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id, event_id=event_id)
        db.add(db_obj)

        # افزایش registered_count
        event.registered_count += 1
        db.add(event)

        db.commit()
        db.refresh(db_obj)

        # ایجاد اطلاعیه
        from app.services.notification_service import notification_service
        notification_service.create_for_user(
            db, user_id=user_id, message=f"You have successfully registered for the event: {event.title}"
        )

        return db_obj

    def remove_registration(self, db: Session, *, user_id: int, event_id: int) -> Optional[EventRegistration]:
        # بررسی ثبت‌نام
        registration = self.get_by_user_and_event(db, user_id=user_id, event_id=event_id)
        if not registration:
            raise HTTPException(status_code=404, detail="Registration not found")

        # کاهش registered_count
        event = db.query(Event).filter(Event.id == event_id).first()
        if event:
            event.registered_count -= 1
            db.add(event)

        db.delete(registration)
        db.commit()

        # ایجاد اطلاعیه
        from app.services.notification_service import notification_service
        notification_service.create_for_user(
            db, user_id=user_id, message=f"You have unregistered from the event: {event.title}"
        )

        return registration

    def get_by_user_and_event(self, db: Session, *, user_id: int, event_id: int) -> Optional[EventRegistration]:
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
