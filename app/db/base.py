# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base, CustomBase  # noqa
from app.models.article import Article  # noqa
from app.models.comment import Comment  # noqa
from app.models.event import Event  # noqa
from app.models.event_registration import EventRegistration  # noqa
from app.models.membership_request import MembershipRequest  # noqa
from app.models.news import News  # noqa
from app.models.notification import Notification  # noqa
from app.models.user import User  # noqa
