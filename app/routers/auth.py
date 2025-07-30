from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.core import security
from app.db.session import get_db
from app.services.user_service import user_service

router = APIRouter()

from sqlalchemy.exc import IntegrityError

@router.post("/signup", response_model=schemas.Token)
def signup(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    try:
        # بررسی ایمیل
        user = user_service.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

        # بررسی شماره دانشجویی
        existing_student = db.query(models.User).filter(models.User.student_id == user_in.student_id).first()
        if existing_student:
            raise HTTPException(
                status_code=400,
                detail="The student ID is already registered.",
            )

        # بررسی شماره تلفن
        if user_in.phone_number:
            existing_phone = db.query(models.User).filter(models.User.phone_number == user_in.phone_number).first()
            if existing_phone:
                raise HTTPException(
                    status_code=400,
                    detail="The phone number is already registered.",
                )
        user = user_service.create(db, obj_in=user_in)

        access_token = security.create_access_token(
            subject=user.email,
            user_id=user.id,
            user_role=user.role.value,
            full_name=user.full_name,
            is_superuser=user.is_superuser,
        )

        return schemas.Token(
            access_token=access_token,
            token_type="bearer",
            user=schemas.User.model_validate(user)
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A user with this email, student ID, or phone number already exists.",
        )

@router.post("/login/access-token", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = user_service.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = security.create_access_token(
        subject=user.email,
        user_id=user.id,
        user_role=user.role.value,
        full_name=user.full_name,
        is_superuser=user.is_superuser,
    )

    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
        user=schemas.User.model_validate(user)  # تبدیل مدل SQLAlchemy به Pydantic
    )

# پشتیبانی از مسیر قدیمی /token (اختیاری)
@router.post("/token", response_model=schemas.Token, include_in_schema=False)
def login_for_access_token_alias(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    return login_for_access_token(db, form_data)
