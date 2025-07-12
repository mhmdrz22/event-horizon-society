from sqlalchemy.orm import Session
from .base import ServiceBase
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate

class ArticleService(ServiceBase[Article, ArticleCreate, ArticleUpdate]):
    def create(self, db: Session, *, obj_in: ArticleCreate, author_id: int) -> Article:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

article_service = ArticleService(Article)
