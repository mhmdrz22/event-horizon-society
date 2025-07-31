import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.services.user_service import user_service
from app.schemas.user import UserCreate
from app.core.security import create_access_token
from app.db.session import SessionLocal

def get_superuser_token_headers(test_client: TestClient, db_session: SessionLocal) -> dict[str, str]:
    email = "admin@example.com"
    password = "adminpassword"
    unique_id = str(uuid.uuid4())[:8]  # یه شناسه یکتا کوتاه
    user = user_service.get_by_email(db_session, email=email)
    if not user:
        user_in = UserCreate(
            email=email,
            password=password,
            full_name="Admin User",
            is_superuser=True,
            student_id=f"ADMIN-{unique_id}"  # student_id یکتا
        )
        user = user_service.create(db_session, obj_in=user_in)
    access_token = create_access_token(
        subject=user.email,
        user_id=user.id,
        user_role=user.role.value,
        full_name=user.full_name,
        is_superuser=user.is_superuser,
    )
    return {"Authorization": f"Bearer {access_token}"}

def get_normal_user_token_headers(test_client: TestClient, db_session: SessionLocal) -> dict[str, str]:
    email = "user@example.com"
    password = "password"
    unique_id = str(uuid.uuid4())[:8]  # یه شناسه یکتا کوتاه
    user_in = UserCreate(
        email=email,
        password=password,
        full_name="Normal User",
        is_superuser=False,
        student_id=f"USER-{unique_id}"  # student_id یکتا
    )
    user = user_service.create(db_session, obj_in=user_in)
    access_token = create_access_token(
        subject=user.email,
        user_id=user.id,
        user_role=user.role.value,
        full_name=user.full_name,
        is_superuser=user.is_superuser,
    )
    return {"Authorization": f"Bearer {access_token}"}
