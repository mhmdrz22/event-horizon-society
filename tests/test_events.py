from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from tests.utils.user import get_normal_user_token_headers, get_superuser_token_headers

def test_create_event_as_admin(client: TestClient, db: Session, superuser_token_headers):
    event_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "event_datetime": "2025-08-01T10:00:00+00:00",
        "location": "Test Location",
        "capacity": 50
    }
    response = client.post(
        f"{settings.API_V1_STR}/events/", headers=superuser_token_headers, json=event_data
    )
    assert response.status_code == 200
    created_event = response.json()
    assert created_event["title"] == event_data["title"]
    assert created_event["capacity"] == event_data["capacity"]

def test_register_for_event(client: TestClient, db: Session, superuser_token_headers, normal_user_token_headers):
    # اول یه رویداد ایجاد کن
    event_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "event_datetime": "2025-08-01T10:00:00+00:00",
        "location": "Test Location",
        "capacity": 50
    }
    response = client.post(
        f"{settings.API_V1_STR}/events/", headers=superuser_token_headers, json=event_data
    )
    event_id = response.json()["id"]

    # ثبت‌نام با کاربر معمولی
    response = client.post(
        f"{settings.API_V1_STR}/events/{event_id}/register", headers=normal_user_token_headers
    )
    assert response.status_code == 200
    registration = response.json()
    assert registration["event_id"] == event_id
