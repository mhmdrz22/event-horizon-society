import io
import os
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from tests.test_utils import get_normal_user_token_headers


def test_create_article(test_client: TestClient, db_session: Session):
    headers = get_normal_user_token_headers(test_client, db_session)
    article_data = {"title": "Test Article", "content": "This is a test article."}
    response = test_client.post(
        f"{settings.API_V1_STR}/articles/",
        headers=headers,
        json=article_data,
    )
    assert response.status_code == 200
    created_article = response.json()
    assert created_article["title"] == article_data["title"]
    assert created_article["content"] == article_data["content"]
    assert "id" in created_article
    assert "author_id" in created_article


def test_upload_article(test_client: TestClient, db_session: Session):
    headers = get_normal_user_token_headers(test_client, db_session)
    article_data = {
        "title": "Test Upload Article",
        "content": "This is a test upload article.",
    }
    file_content = b"This is a test PDF file."
    files = {"file": ("test.pdf", io.BytesIO(file_content), "application/pdf")}

    response = test_client.post(
        f"{settings.API_V1_STR}/articles/upload",
        headers=headers,
        data=article_data,
        files=files,
    )

    assert response.status_code == 200
    created_article = response.json()
    assert created_article["title"] == article_data["title"]
    assert created_article["content"] == article_data["content"]
    assert "file_path" in created_article
    assert created_article["file_path"] is not None

    # Check if the file was saved
    file_path = created_article["file_path"]
    assert os.path.exists(file_path)

    # Clean up the created file
    os.remove(file_path)
