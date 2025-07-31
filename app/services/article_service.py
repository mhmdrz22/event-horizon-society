import os
import shutil
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from .base import ServiceBase
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate

UPLOAD_DIR = "uploads/articles"

class ArticleService(ServiceBase[Article, ArticleCreate, ArticleUpdate]):
    def create(self, db: Session, *, obj_in: ArticleCreate, author_id: int) -> Article:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_with_file(
        self, db: Session, *, obj_in: ArticleCreate, file: UploadFile, author_id: int
    ) -> Article:
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Create a unique filename to prevent collisions
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create article entry in the database
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, author_id=author_id, file_path=file_path)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def update_status(self, db: Session, *, article_id: int, status: str) -> Article:
        article = self.get(db, id=article_id)
        if article:
            article.status = status
            db.commit()
            db.refresh(article)
        return article

article_service = ArticleService(Article)
