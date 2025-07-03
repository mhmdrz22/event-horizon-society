from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime
from app.models.news import NewsStatus as ModelNewsStatus # Enum from model
from .user import User # For embedding author information

class NewsBase(BaseModel):
    title: constr(min_length=1, max_length=255)
    content: str

class NewsCreate(NewsBase):
    status: Optional[ModelNewsStatus] = ModelNewsStatus.DRAFT # Default status on creation

class NewsUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=255)] = None
    content: Optional[str] = None
    status: Optional[ModelNewsStatus] = None

class News(NewsBase):
    id: int
    author_id: int
    status: ModelNewsStatus
    created_at: datetime
    updated_at: datetime
    author: Optional[User] = None # Embed author details in response

    # Pydantic V2 compatibility
    model_config = {"from_attributes": True}
