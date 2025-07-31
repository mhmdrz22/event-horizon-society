from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user, get_current_student_user
from app.db.session import get_db
from app.services.article_service import article_service

router = APIRouter()

@router.get("/", response_model=List[schemas.Article])
def read_articles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve articles.
    """
    articles = article_service.get_multi(db, skip=skip, limit=limit)
    return articles

@router.post("/upload", response_model=schemas.Article)
def upload_article(
    *,
    db: Session = Depends(get_db),
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_student_user),
) -> Any:
    """
    Upload a new article with a file. Accessible only by students.
    """
    # Create a schema for article creation data
    article_in = schemas.ArticleCreate(title=title, content=content)

    # The service will handle file saving and article creation
    article = article_service.create_with_file(
        db=db, obj_in=article_in, file=file, author_id=current_user.id
    )
    return article


@router.post("/", response_model=schemas.Article)
def create_article(
    *,
    db: Session = Depends(get_db),
    article_in: schemas.ArticleCreate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Create new article.
    """
    article = article_service.create(db=db, obj_in=article_in, author_id=current_user.id)
    return article

@router.get("/{article_id}", response_model=schemas.Article)
def read_article_by_id(
    article_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get article by ID.
    """
    article = article_service.get(db=db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/{article_id}", response_model=schemas.Article)
def update_article(
    *,
    db: Session = Depends(get_db),
    article_id: int,
    article_in: schemas.ArticleUpdate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Update an article.
    """
    article = article_service.get(db=db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    # Authorization: only admin can update article status
    if current_user.role != models.user.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    article = article_service.update(db=db, db_obj=article, obj_in=article_in)
    return article

@router.delete("/{article_id}", response_model=schemas.Article)
def delete_article(
    *,
    db: Session = Depends(get_db),
    article_id: int,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Delete an article.
    """
    article = article_service.get(db=db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    # Authorization: only admin or author can delete
    if article.author_id != current_user.id and current_user.role != models.user.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    article = article_service.remove(db=db, id=article_id)
    return article
