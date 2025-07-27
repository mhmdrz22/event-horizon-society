import sqlalchemy
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    Enum,
    ForeignKey,
    Time,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
import enum


# Define the Base
Base = declarative_base()

# Define Enums
class UserRole(enum.Enum):
    STUDENT = "دانشجو"
    ASSOCIATION_MEMBER = "عضو انجمن"
    ASSOCIATION_ADMIN = "مدیر انجمن"

class NewsStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"

class ArticleStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class MembershipRequestStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# Define Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    student_id = Column(String(50), unique=True, index=True, nullable=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    news_items = relationship("News", back_populates="author", cascade="all, delete-orphan")
    events_organized = relationship("Event", back_populates="organizer", cascade="all, delete-orphan")
    event_registrations = relationship("EventRegistration", back_populates="user", cascade="all, delete-orphan")
    articles = relationship("Article", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    membership_requests = relationship("MembershipRequest", back_populates="user", cascade="all, delete-orphan")

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum(NewsStatus), default=NewsStatus.DRAFT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="news_items")
    comments = relationship("Comment", back_populates="news_item", cascade="all, delete-orphan")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_datetime = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    registered_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organizer = relationship("User", back_populates="events_organized")
    registrations = relationship("EventRegistration", back_populates="event", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="event_item", cascade="all, delete-orphan")
    __table_args__ = (
        CheckConstraint('registered_count <= capacity', name='cc_registered_count_less_than_equal_capacity'),
        CheckConstraint('capacity > 0', name='cc_capacity_positive'),
        CheckConstraint('registered_count >= 0', name='cc_registered_count_non_negative'),
    )

class EventRegistration(Base):
    __tablename__ = "event_registrations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user = relationship("User", back_populates="event_registrations")
    event = relationship("Event", back_populates="registrations")
    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='uq_user_event_registration'),
    )

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum(ArticleStatus), default=ArticleStatus.PENDING, nullable=False)
    review_comments = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="articles")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="comments")
    news_id = Column(Integer, ForeignKey("news.id"), nullable=True)
    news_item = relationship("News", back_populates="comments")
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)
    event_item = relationship("Event", back_populates="comments")
    __table_args__ = (
        CheckConstraint('(news_id IS NOT NULL AND event_id IS NULL) OR (news_id IS NULL AND event_id IS NOT NULL)', name='cc_comment_target_xor'),
    )

class MembershipRequest(Base):
    __tablename__ = "membership_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Enum(MembershipRequestStatus), default=MembershipRequestStatus.PENDING, nullable=False)
    requested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    user = relationship("User", back_populates="membership_requests")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")


# Create the engine
engine = create_engine("sqlite:///./test.db")

# Create the tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created.")

# Verify the tables
print("\nVerifying tables...")
conn = engine.connect()
meta = MetaData()
meta.reflect(bind=conn)
print("Tables in database:", meta.tables.keys())
conn.close()
