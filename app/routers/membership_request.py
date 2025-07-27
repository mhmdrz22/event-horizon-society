from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user
from app.db.session import get_db
from app.services.membership_request_service import membership_request_service

router = APIRouter()

@router.get("/", response_model=List[schemas.MembershipRequest])
def read_membership_requests(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Retrieve membership requests. Admins see all, users see their own.
    """
    if current_user.role == models.user.UserRole.ASSOCIATION_ADMIN:
        requests = membership_request_service.get_multi(db, skip=skip, limit=limit)
    else:
        requests = membership_request_service.get_multi_by_user(
            db, user_id=current_user.id, skip=skip, limit=limit
        )
    return requests

@router.post("/", response_model=schemas.MembershipRequest)
def create_membership_request(
    *,
    db: Session = Depends(get_db),
    request_in: schemas.MembershipRequestCreate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Create new membership request.
    """
    # Add logic to prevent duplicate requests if needed
    request = membership_request_service.create(db=db, obj_in=request_in, user_id=current_user.id)
    return request

@router.put("/{request_id}", response_model=schemas.MembershipRequest)
def update_membership_request(
    *,
    db: Session = Depends(get_db),
    request_id: int,
    request_in: schemas.MembershipRequestUpdate,
    current_user: models.user.User = Depends(get_current_user),
) -> Any:
    """
    Update a membership request (Approve/Reject).
    """
    if current_user.role != models.user.UserRole.ASSOCIATION_ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    request = membership_request_service.get(db=db, id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request = membership_request_service.update(db=db, db_obj=request, obj_in=request_in)
    return request
