from app.db.session import SessionLocal
from app.models import user, news, article, event, event_registration, comment, membership_request, notification
from app.models.user import User
from app.core.security import get_password_hash

def create_superuser():
    db = SessionLocal()
    try:
        # Check if a superuser already exists
        if db.query(User).filter(User.is_superuser).first():
            print("Superuser already exists.")
            return

        superuser = User(
            full_name="Admin User",
            email="admin@example.com",
            password_hash=get_password_hash("admin"),
            is_superuser=True,
            is_active=True,
        )
        db.add(superuser)
        db.commit()
        print("Superuser created successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    create_superuser()
