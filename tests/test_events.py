from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate

def test_create_event_as_admin(test_client: TestClient, db_session: Session, superuser_token_headers):
    event_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "event_datetime": "2025-08-01T10:00:00",
        "location": "Test Location",
        "capacity": 50
    }
    response = test_client.post("/api/v1/events/", json=event_data, headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Event"

def test_register_for_event(test_client: TestClient, db_session: Session, superuser_token_headers, normal_user_token_headers):
    event_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "event_datetime": "2025-08-01T10:00:00",
        "location": "Test Location",
        "capacity": 50
    }
    response = test_client.post("/api/v1/events/", json=event_data, headers=superuser_token_headers)
    assert response.status_code == 200
    event_id = response.json()["id"]

    response = test_client.post(f"/api/v1/events/{event_id}/register", headers=normal_user_token_headers)
    assert response.status_code == 200
