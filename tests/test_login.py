from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.test_utils import get_normal_user_token_headers


def test_login_for_access_token(test_client: TestClient, db_session: Session):
    headers = get_normal_user_token_headers(test_client, db_session)
    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Bearer ")
