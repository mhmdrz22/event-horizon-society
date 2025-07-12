from sqlalchemy.orm import Session
from .base import ServiceBase
from app.models.membership_request import MembershipRequest
from app.schemas.membership_request import MembershipRequestCreate, MembershipRequestUpdate

from typing import List

class MembershipRequestService(ServiceBase[MembershipRequest, MembershipRequestCreate, MembershipRequestUpdate]):
    def create(self, db: Session, *, obj_in: MembershipRequestCreate, user_id: int) -> MembershipRequest:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[MembershipRequest]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

membership_request_service = MembershipRequestService(MembershipRequest)
