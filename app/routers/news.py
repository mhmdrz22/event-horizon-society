from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user
from app.db.session import get_db
from app.services.news_service import news_service

router = APIRouter()

@router.get("/", response_model=List[schemas.News])
def read_news(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve news.
    """
    news = news_service.get_multi(db, skip=skip, limit=limit)
    return news

@router.post("/", response_model=schemas.News)
def create_news(
    *,
    db: Session = Depends(get_db),
    news_in: schemas.NewsCreate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Create new news item.
    """
    # We need to add the author_id from the current user
    news = news_service.create(db=db, obj_in=news_in, author_id=current_user.id)
    return news

@router.get("/{news_id}", response_model=schemas.News)
def read_news_by_id(
    news_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get news by ID.
    """
    news = news_service.get(db=db, id=news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.put("/{news_id}", response_model=schemas.News)
def update_news(
    *,
    db: Session = Depends(get_db),
    news_id: int,
    news_in: schemas.NewsUpdate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Update a news item.
    """
    news = news_service.get(db=db, id=news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    # Add authorization logic here if needed, e.g. only author or admin can update
    # if news.author_id != current_user.id and current_user.role != "admin":
    #     raise HTTPException(status_code=403, detail="Not enough permissions")
    news = news_service.update(db=db, db_obj=news, obj_in=news_in)
    return news

@router.delete("/{news_id}", response_model=schemas.News)
def delete_news(
    *,
    db: Session = Depends(get_db),
    news_id: int,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Delete a news item.
    """
    news = news_service.get(db=db, id=news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    # Add authorization logic here as well
    # if news.author_id != current_user.id and current_user.role != "admin":
    #     raise HTTPException(status_code=403, detail="Not enough permissions")
    news = news_service.remove(db=db, id=news_id)
    return news
