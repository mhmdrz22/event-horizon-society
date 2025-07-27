from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user
from app.database import get_db
from app.services.comment_service import comment_service

router = APIRouter()

from typing import Optional

@router.get("/", response_model=List[schemas.Comment])
def read_comments(
    db: Session = Depends(get_db),
    news_id: Optional[int] = None,
    event_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve comments, optionally filtered by news_id or event_id.
    """
    # This requires a custom service method
    comments = comment_service.get_multi_filtered(
        db, news_id=news_id, event_id=event_id, skip=skip, limit=limit
    )
    return comments

@router.post("/", response_model=schemas.Comment)
def create_comment(
    *,
    db: Session = Depends(get_db),
    comment_in: schemas.CommentCreate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Create new comment.
    """
    comment = comment_service.create(db=db, obj_in=comment_in, user_id=current_user.id)
    return comment

@router.delete("/{comment_id}", response_model=schemas.Comment)
def delete_comment(
    *,
    db: Session = Depends(get_db),
    comment_id: int,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Delete a comment.
    """
    comment = comment_service.get(db=db, id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id and current_user.role != models.user.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = comment_service.remove(db=db, id=comment_id)
    return comment
