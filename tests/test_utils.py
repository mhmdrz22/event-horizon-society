from fastapi.testclient import TestClient
from app.core.config import settings
from app.schemas.user import UserCreate
from app.services.user_service import user_service
from app.db.session import SessionLocal

def get_superuser_token_headers(client: TestClient, db_session: SessionLocal) -> dict[str, str]:
    email = "admin@example.com"
    password = "adminpassword"
    user = user_service.get_by_email(db_session, email=email)
    if not user:
        user_in = UserCreate(
            email=email,
            password=password,
            full_name="Admin User",
            is_superuser=True,
        )
        user = user_service.create(db_session, obj_in=user_in)
    elif not user.is_superuser:
        user.is_superuser = True
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)


    login_data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers

def get_normal_user_token_headers(client: TestClient, db_session: SessionLocal) -> dict[str, str]:
    email = "user@example.com"
    password = "password"
    user_in = UserCreate(
        email=email,
        password=password,
        full_name="Normal User",
        is_superuser=False,
    )
    user = user_service.get_by_email(db_session, email=email)
    if not user:
        user = user_service.create(db_session, obj_in=user_in)

    login_data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
