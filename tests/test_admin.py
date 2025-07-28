from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.schemas.user import UserCreate
from app.services.user_service import user_service
from tests.test_utils import get_superuser_token_headers, get_normal_user_token_headers


def test_get_users_as_superuser(test_client: TestClient, db_session: Session):
    headers = get_superuser_token_headers(test_client, db_session)
    r = test_client.get(f"{settings.API_V1_STR}/users/", headers=headers)
    all_users = r.json()
    assert r.status_code == 200
    assert len(all_users) > 1
    for user in all_users:
        assert "email" in user


def test_get_articles_as_superuser(test_client: TestClient, db_session: Session):
    headers = get_superuser_token_headers(test_client, db_session)
    r = test_client.get(f"{settings.API_V1_STR}/articles/", headers=headers)
    assert r.status_code == 200


def test_get_users_as_normal_user(test_client: TestClient, db_session: Session):
    headers = get_normal_user_token_headers(test_client, db_session)
    r = test_client.get(f"{settings.API_V1_STR}/users/", headers=headers)
    assert r.status_code == 403


def test_get_articles_as_normal_user(test_client: TestClient, db_session: Session):
    headers = get_normal_user_token_headers(test_client, db_session)
    r = test_client.get(f"{settings.API_V1_STR}/articles/", headers=headers)
    assert r.status_code == 200


def test_update_user_status(test_client: TestClient, db_session: Session):
    headers = get_superuser_token_headers(test_client, db_session)
    get_normal_user_token_headers(test_client, db_session)
    user = user_service.get_by_email(db_session, email="user@example.com")
    assert user
    response = test_client.put(
        f"{settings.API_V1_STR}/users/{user.id}/status",
        headers=headers,
        json={"is_active": False},
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["is_active"] is False


def test_superuser_creation(test_client: TestClient, db_session: Session):
    headers = get_superuser_token_headers(test_client, db_session)
    r = test_client.get(f"{settings.API_V1_STR}/users/me", headers=headers)
    assert r.status_code == 200
    user = r.json()
    assert user["is_superuser"] is True
