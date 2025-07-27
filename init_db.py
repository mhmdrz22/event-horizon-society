from app.core.config import settings
from sqlalchemy import create_engine

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI.replace("sqlite:///./", "sqlite:///"),
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} # Needed for SQLite
)
from app.db.base import Base
from app.models import user, news, article, event, event_registration, comment, membership_request, notification

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    init_db()
