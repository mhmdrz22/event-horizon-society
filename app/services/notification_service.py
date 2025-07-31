from typing import List
from sqlalchemy.orm import Session
from .base import ServiceBase
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate

class NotificationService(ServiceBase[Notification, NotificationCreate, NotificationUpdate]):
    def create_for_user(self, db: Session, *, user_id: int, message: str) -> Notification:
        obj_in = NotificationCreate(user_id=user_id, message=message)
        return self.create(db, obj_in=obj_in)

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def mark_all_as_read(self, db: Session, *, user_id: int) -> int:
        num_updated = (
            db.query(self.model)
            .filter(self.model.user_id == user_id, self.model.is_read == False)
            .update({"is_read": True}, synchronize_session=False)
        )
        db.commit()
        return num_updated

    def delete_read_notifications(self, db: Session, *, user_id: int) -> int:
        num_deleted = (
            db.query(self.model)
            .filter(self.model.user_id == user_id, self.model.is_read == True)
            .delete(synchronize_session=False)
        )
        db.commit()
        return num_deleted

notification_service = NotificationService(Notification)
