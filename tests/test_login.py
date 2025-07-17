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

def test_login_for_access_token():
    # Create a test user
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={"email": "test@example.com", "password": "testpassword", "full_name": "Test User"},
    )
    assert response.status_code == 200

    # Test login
    response = client.post(
        f"{settings.API_V1_STR}/auth/login/access-token",
        data={"username": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"
