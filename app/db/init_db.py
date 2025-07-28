import logging
from sqlalchemy import create_engine
from app.core.config import settings
from app.db.base import Base
from app.models import user, news, article, comment, event, event_registration, membership_request
from app.schemas.user import UserCreate
from app.services.user_service import user_service
from app.db.session import SessionLocal
from app.models.user import User, UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """
    Initializes the database by creating a superuser if it doesn't exist.
    """
    try:
        db = SessionLocal()
        # Check if a superuser already exists
        if user_service.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL):
            logger.info("Superuser with this email already exists.")
            return

        superuser_in = UserCreate(
            full_name=settings.FIRST_SUPERUSER_FULL_NAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            role=UserRole.ASSOCIATION_ADMIN,
            is_superuser=True,
            is_active=True,
        )
        user_service.create(db, obj_in=superuser_in)
        logger.info("Superuser created successfully.")
        db.close()

    except Exception as e:
        logger.error(f"An error occurred during database initialization: {e}")
        raise

if __name__ == "__main__":
    logger.info("Initializing the database...")
    init_db()
    logger.info("Database initialization finished.")
