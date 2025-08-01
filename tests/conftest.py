import pytest
import os

# This must be the very first thing to run, to ensure all subsequent imports see the TESTING flag.
os.environ["TESTING"] = "True"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings # Now this will load with TESTING=True
from fastapi.testclient import TestClient


# Create the test engine using the in-memory SQLite URL from settings
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False} # Needed for SQLite in-memory
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Create a new database session for each test, with a clean database.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """
    Create a test client that uses the test database.
    """
    from app.main import app # Lazy import

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


from tests.test_utils import get_normal_user_token_headers, get_superuser_token_headers
from sqlalchemy.orm import Session

@pytest.fixture(scope="function")
def superuser_token_headers(test_client: TestClient, db_session: Session):
    return get_superuser_token_headers(test_client, db_session)

@pytest.fixture(scope="function")
def normal_user_token_headers(test_client: TestClient, db_session: Session):
    return get_normal_user_token_headers(test_client, db_session)
