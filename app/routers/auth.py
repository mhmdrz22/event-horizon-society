from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.core import security
from app.db.session import get_db
from app.services.user_service import user_service

router = APIRouter()

@router.post("/signup", response_model=schemas.Token)
def signup(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = user_service.get_by_email(db, email=user_in.email)
    if not user:
        user = user_service.create(db, obj_in=user_in)
    elif not user.is_superuser:
        # This allows promoting an existing user to superuser
        # as a simple way to bootstrap the first admin user.
        user.is_superuser = user_in.is_superuser
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    access_token = security.create_access_token(
        subject=user.email,
        user_id=user.id,
        user_role=user.role.value,
        full_name=user.full_name,
        is_superuser=user.is_superuser,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
       from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.core import security
from app.db.session import get_db
from app.services.user_service import user_service

router = APIRouter()

@router.post("/signup", response_model=schemas.Token)
def signup(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = user_service.get_by_email(db, email=user_in.email)
    if not user:
        user = user_service.create(db, obj_in=user_in)
    elif not user.is_superuser:
        # This allows promoting an existing user to superuser
        # as a simple way to bootstrap the first admin user.
        user.is_superuser = user_in.is_superuser
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    access_token = security.create_access_token(
        subject=user.email,
        user_id=user.id,
        user_role=user.role.value,
        full_name=user.full_name,
        is_superuser=user.is_superuser,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
       "user": schemas.User.model_validate(user),
    }


@router.post("/token")
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
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
       
    }


@router.post("/token")
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
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
