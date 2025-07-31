from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_get_notifications(test_client: TestClient, db_session: Session, normal_user_token_headers):
    response = test_client.get("/api/v1/notifications/", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_mark_all_notifications_as_read(test_client: TestClient, db_session: Session, normal_user_token_headers):
    response = test_client.post("/api/v1/notifications/mark-all-read", headers=normal_user_token_headers)
    assert response.status_code == 200
