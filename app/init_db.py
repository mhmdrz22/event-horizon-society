import logging
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import engine
from app.db.base import Base
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    """
    Initialize the database by creating all tables defined in SQLAlchemy models.
    """
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        # Optionally, re-raise the exception if you want the script to fail
        # raise e

if __name__ == "__main__":
    logger.info(f"Initializing database at {settings.DATABASE_URL}")
    init_db()
