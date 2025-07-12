from .base import ServiceBase
from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate

from sqlalchemy.orm import Session
from app.schemas.news import NewsCreate
from app.models.news import News

class NewsService(ServiceBase[News, NewsCreate, NewsUpdate]):
    def create(self, db: Session, *, obj_in: NewsCreate, author_id: int) -> News:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

news_service = NewsService(News)
