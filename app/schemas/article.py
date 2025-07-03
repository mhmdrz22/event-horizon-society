from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime
from app.models.article import ArticleStatus as ModelArticleStatus # Enum from model
from .user import User # For embedding author information

class ArticleBase(BaseModel):
    title: constr(min_length=1, max_length=255)
    content: str

class ArticleCreate(ArticleBase):
    # author_id will be set from the authenticated user
    # status will default to PENDING in the model or service layer
    pass

class ArticleUpdate(BaseModel): # For admin review
    status: ModelArticleStatus
    review_comments: Optional[str] = None

class Article(ArticleBase):
    id: int
    author_id: int
    status: ModelArticleStatus
    review_comments: Optional[str] = None
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    author: Optional[User] = None # Embed author details

    # Pydantic V2 compatibility
    model_config = {"from_attributes": True}
