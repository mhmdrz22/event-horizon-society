from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user_service import user_service


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    # Create a superuser
    email = "admin@example.com"
    password = "password"
    user_in = UserCreate(
        email=email,
        password=password,
        full_name="Admin User",
        is_superuser=True,
    )
    # A bit of a hack to create the user directly without going through the API
    # This is to avoid having to deal with the case where the user already exists
    with Session(settings.TEST_SQLALCHEMY_DATABASE_URI) as db:
        user_service.create(db, obj_in=user_in)

    # Get a token for the superuser
    login_data = {
        "username": email,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def test_get_users_as_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/admin/users", headers=superuser_token_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_articles_as_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/admin/articles", headers=superuser_token_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
