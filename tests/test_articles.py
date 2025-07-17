import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def get_auth_token():
    # Create a test user
    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "test-article@example.com", "password": "testpassword", "full_name": "Test User"},
    )
    # Test login
    response = client.post(
        f"{settings.API_V1_STR}/auth/login/access-token",
        data={"username": "test-article@example.com", "password": "testpassword"},
    )
    token = response.json()["access_token"]
    return token

def test_create_article():
    token = get_auth_token()
    response = client.post(
        f"{settings.API_V1_STR}/articles/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Article", "content": "This is a test article with more than fifty characters."},
    )
    assert response.status_code == 200
    article = response.json()
    assert article["title"] == "Test Article"
    assert article["content"] == "This is a test article with more than fifty characters."
    assert "id" in article
    assert "author_id" in article
