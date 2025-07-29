from sqlalchemy.orm import Session
from .base import ServiceBase
from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate

class NewsService(ServiceBase[News, NewsCreate, NewsUpdate]):
    def create(self, db: Session, *, obj_in: NewsCreate, author_id: int) -> News:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # اطلاعیه برای انتشار خبر (اگر منتشر شده باشد)
        if db_obj.status == "published":
            from app.services.notification_service import notification_service
            notification_service.create_for_user(
                db, user_id=author_id, message=f"Your news '{db_obj.title}' has been published."
            )

        return db_obj

    def update(self, db: Session, *, db_obj: News, obj_in: NewsUpdate) -> News:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "status" in update_data and update_data["status"] == "published":
            from app.services.notification_service import notification_service
            notification_service.create_for_user(
                db, user_id=db_obj.author_id, message=f"Your news '{db_obj.title}' has been published."
            )
        return super().update(db, db_obj=db_obj, obj_in=update_data)

news_service = NewsService(News)
