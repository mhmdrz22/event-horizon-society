# This file is used to ensure all SQLAlchemy models are imported before initializing DB.
# This allows Base.metadata.create_all(engine) to know about all tables.

from app.db.base_class import Base  # Import the Base class

# Import all the models, so that Base has them before being
# imported by Alembic or used by create_all / Main init script
# These will be created in subsequent steps.
# For now, we'll add comments as placeholders.
from app.models.user import User
from app.models.news import News
from app.models.event import Event
from app.models.event_registration import EventRegistration
from app.models.article import Article
from app.models.comment import Comment
from app.models.membership_request import MembershipRequest
