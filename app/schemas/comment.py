from pydantic import BaseModel, model_validator # Will be changed to model_validator
from typing import Optional
from datetime import datetime
from .user import User # For embedding author information

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    # user_id will be set from the authenticated user
    news_id: Optional[int] = None
    event_id: Optional[int] = None

    @model_validator(mode="before") # Pydantic v1 style, ensure v2 compatibility or adjust

    def check_news_or_event_id_present(cls, values):
        news_id, event_id = values.get('news_id'), values.get('event_id')
        if news_id is not None and event_id is not None:
            raise ValueError('Cannot provide both news_id and event_id')
        if news_id is None and event_id is None:
            raise ValueError('Either news_id or event_id must be provided')
        return values

class Comment(CommentBase):
    id: int
    user_id: int
    news_id: Optional[int] = None
    event_id: Optional[int] = None
    created_at: datetime
    author: Optional[User] = None # Embed author details

    # Pydantic V2 compatibility
    model_config = {"from_attributes": True}
