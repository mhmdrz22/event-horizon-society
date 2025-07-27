# This file is kept for backwards compatibility.
# New code should import from app.db.session and app.db.base.
from .db.session import SessionLocal, engine, get_db
from .db.base import Base
