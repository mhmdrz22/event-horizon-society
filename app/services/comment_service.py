from sqlalchemy.orm import Session
from .base import ServiceBase
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

from typing import List, Optional

class CommentService(ServiceBase[Comment, CommentCreate, None]): # No Update schema for comments
    def create(self, db: Session, *, obj_in: CommentCreate, user_id: int) -> Comment:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_filtered(
        self, db: Session, *, news_id: Optional[int], event_id: Optional[int], skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        query = db.query(self.model)
        if news_id:
            query = query.filter(self.model.news_id == news_id)
        if event_id:
            query = query.filter(self.model.event_id == event_id)
        return query.offset(skip).limit(limit).all()

comment_service = CommentService(Comment)
