from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import user_service
from app.core.security import get_current_user
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class UserStatusUpdate(BaseModel):
    is_active: bool

@router.get("/", response_model=list[dict])
async def get_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    users = user_service.get_all(db)
    return users

@router.put("/{user_id}/status")
async def update_user_status(
    user_id: int,
    status: UserStatusUpdate,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db),
):
    user = user_service.get_by_id(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = status.is_active
    db.commit()
    db.refresh(user)
    return {"message": "User status updated"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
