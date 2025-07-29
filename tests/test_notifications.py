from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from tests.utils.user import get_normal_user_token_headers

def test_get_notifications(client: TestClient, db: Session, normal_user_token_headers):
    response = client.get(f"{settings.API_V1_STR}/notifications/", headers=normal_user_token_headers)
    assert response.status_code == 200
    notifications = response.json()
    assert isinstance(notifications, list)

def test_mark_all_notifications_as_read(client: TestClient, db: Session, normal_user_token_headers):
    response = client.post(
        f"{settings.API_V1_STR}/notifications/mark-all-read", headers=normal_user_token_headers
    )
    assert response.status_code == 200
    assert response.json() >= 0  # تعداد اطلاعیه‌های به‌روزرسانی‌شده
