from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import schemas
from app.core.config import settings
from tests.test_utils import create_random_user

def test_get_users_superuser(
    test_client: TestClient, superuser_token_headers: dict, db_session: Session
):
    create_random_user(db_session)
    create_random_user(db_session)
    response = test_client.get(
        f"{settings.API_V1_STR}/admin/users", headers=superuser_token_headers
    )
    assert response.status_code == 200
    all_users = response.json()
    # The first user is the superuser, then we create two more
    assert len(all_users) >= 3
    for user in all_users:
        assert "email" in user


def test_update_user_status_superuser(
    test_client: TestClient, superuser_token_headers: dict, db_session: Session
):
    user = create_random_user(db_session)
    assert user.is_active is True

    # Deactivate user
    response = test_client.put(
        f"{settings.API_V1_STR}/admin/users/{user.id}/status",
        headers=superuser_token_headers,
        json={"is_active": False},
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["is_active"] is False

    # Activate user
    response = test_client.put(
        f"{settings.API_V1_STR}/admin/users/{user.id}/status",
        headers=superuser_token_headers,
        json={"is_active": True},
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["is_active"] is True


def test_get_users_normal_user(
    test_client: TestClient, normal_user_token_headers: dict, db_session: Session
):
    response = test_client.get(
        f"{settings.API_V1_STR}/admin/users", headers=normal_user_token_headers
    )
    assert response.status_code == 403


def test_update_user_status_normal_user(
    test_client: TestClient, normal_user_token_headers: dict, db_session: Session
):
    user = create_random_user(db_session)
    response = test_client.put(
        f"{settings.API_V1_STR}/admin/users/{user.id}/status",
        headers=normal_user_token_headers,
        json={"is_active": False},
    )
    assert response.status_code == 403
