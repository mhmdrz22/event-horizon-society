import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.main import app
from app.models.user import User
from app.models.article import Article
from app.schemas.user import UserCreate
from app.services.user_service import user_service
from app.db.session import SessionLocal, engine
from app.db.base import Base

@pytest.fixture(scope="function")
def db_session():
    """
    Creates a new database session for each test function.
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_client():
    """
    Creates a TestClient instance.
    """
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")
def superuser_token_headers(test_client: TestClient, db_session: Session):
    """
    Creates a superuser and returns the token headers.
    """
    email = "admin@example.com"
    password = "password"
    user_in = UserCreate(
        email=email,
        password=password,
        full_name="Admin User",
        is_superuser=True,
    )
    user_service.create(db_session, obj_in=user_in)

    login_data = {
        "username": email,
        "password": password,
    }
    r = test_client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers

@pytest.fixture(scope="function")
def normal_user_token_headers(test_client: TestClient, db_session: Session):
    """
    Creates a normal user and returns the token headers.
    """
    email = "user@example.com"
    password = "password"
    user_in = UserCreate(
        email=email,
        password=password,
        full_name="Normal User",
        is_superuser=False,
    )
    user_service.create(db_session, obj_in=user_in)

    login_data = {
        "username": email,
        "password": password,
    }
    r = test_client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers

@pytest.fixture(scope="function")
def test_data(db_session: Session):
    """
    Creates some initial data for testing.
    """
    user1 = User(email="test1@example.com", password_hash="test1", full_name="Test User 1", is_superuser=False)
    user2 = User(email="test2@example.com", password_hash="test2", full_name="Test User 2", is_superuser=False)
    db_session.add(user1)
    db_session.add(user2)

    article1 = Article(title="Test Article 1", content="Test Content 1", author_id=user1.id)
    article2 = Article(title="Test Article 2", content="Test Content 2", author_id=user2.id)
    db_session.add(article1)
    db_session.add(article2)

    db_session.commit()

def test_get_users_as_superuser(
    test_client: TestClient, superuser_token_headers: dict[str, str], test_data
) -> None:
    r = test_client.get(f"{settings.API_V1_STR}/admin/users", headers=superuser_token_headers)
    assert r.status_code == 200
    assert len(r.json()) == 3  # 2 test users + 1 superuser

def test_get_articles_as_superuser(
    test_client: TestClient, superuser_token_headers: dict[str, str], test_data
) -> None:
    r = test_client.get(f"{settings.API_V1_STR}/admin/articles", headers=superuser_token_headers)
    assert r.status_code == 200
    assert len(r.json()) == 2

def test_get_users_as_normal_user(
    test_client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = test_client.get(f"{settings.API_V1_STR}/admin/users", headers=normal_user_token_headers)
    assert r.status_code == 403

def test_get_articles_as_normal_user(
    test_client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = test_client.get(f"{settings.API_V1_STR}/admin/articles", headers=normal_user_token_headers)
    assert r.status_code == 403

def test_update_user_status(
    test_client: TestClient, superuser_token_headers: dict[str, str], db_session: Session
) -> None:
    user = db_session.query(User).filter(User.email == "test1@example.com").first()
    r = test_client.put(
        f"{settings.API_V1_STR}/admin/users/{user.id}/status",
        headers=superuser_token_headers,
        params={"is_active": False},
    )
    assert r.status_code == 200
    assert r.json()["is_active"] is False
