from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, services
from app.db.session import get_db
from app.dependencies import get_current_active_superuser

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_active_superuser)],
    responses={404: {"description": "Not found"}},
)


@router.get("/articles", response_model=List[schemas.Article])
def read_articles(db: Session = Depends(get_db)):
    """
    Retrieve all articles.
    """
    articles = services.article_service.get_all(db)
    return articles


@router.put("/articles/{article_id}/status", response_model=schemas.Article)
def update_article_status(
    article_id: int,
    status: schemas.ArticleStatus,
    db: Session = Depends(get_db),
):
    """
    Update an article's status.
    """
    article = services.article_service.update_status(
        db=db, article_id=article_id, status=status
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


