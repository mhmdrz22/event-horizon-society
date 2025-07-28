import logging
from sqlalchemy import create_engine
from app.core.config import settings
from app.db.base import Base
from app.models import user, news
from app.schemas.user import UserCreate
from app.services.user_service import user_service
from app.db.session import SessionLocal
from app.models.user import User, UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """
    Initializes the database. If tables already exist, they will be dropped and recreated.
    """
    try:
        engine = create_engine(
            settings.SQLALCHEMY_DATABASE_URI,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False}  # Needed for SQLite
        )

        logger.info("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("Tables dropped.")

        logger.info("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")

        db = SessionLocal()
        # Check if a superuser already exists
        if user_service.get_by_email(db, email="admin@example.com"):
            logger.info("Superuser with this email already exists.")
            return

        superuser_in = UserCreate(
            full_name="Admin User",
            email="admin@example.com",
            password="adminpassword",
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
