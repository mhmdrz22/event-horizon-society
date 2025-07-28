from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from .base import ServiceBase

class UserService(ServiceBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, *, id: int) -> Optional[User]:
        user = db.query(User).filter(User.id == id).first()
        print(f"Queried user with id {id}: {user}")
        return user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            full_name=obj_in.full_name,
            password_hash=get_password_hash(obj_in.password),
            student_id=obj_in.student_id,
            phone_number=obj_in.phone_number,
            role=obj_in.role,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def update_status(self, db: Session, *, user_id: int, is_active: bool) -> Optional[User]:
        print(f"Updating user {user_id} to is_active={is_active}")
        user = self.get(db, id=user_id)
        if user:
            user.is_active = is_active
            db.add(user)
            db.commit()
            db.refresh(user)
        return user


user_service = UserService(User)
