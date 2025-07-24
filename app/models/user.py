import enum
from sqlalchemy import Column, String, DateTime, Enum as DBEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class UserRole(enum.Enum):
    STUDENT = "دانشجو"
    ASSOCIATION_MEMBER = "عضو انجمن"
    ASSOCIATION_ADMIN = "مدیر انجمن"

class User(Base):
    __tablename__ = "users" # Explicitly defining, though Base would default to "users"

    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    student_id = Column(String(50), unique=True, index=True, nullable=True) # Assuming student_id can be optional for some users initially
    phone_number = Column(String(20), unique=True, index=True, nullable=True) # Assuming phone_number can be optional

    role = Column(DBEnum(UserRole), default=UserRole.STUDENT, nullable=False)
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

    # Relationships will be added later as other models are defined
    # e.g., news_items = relationship("News", back_populates="author")
    # e.g., events_organized = relationship("Event", back_populates="organizer")
    # e.g., event_registrations = relationship("EventRegistration", back_populates="user")
    # e.g., articles = relationship("Article", back_populates="author")
    # e.g., comments = relationship("Comment", back_populates="user")
    # e.g., membership_requests = relationship("MembershipRequest", back_populates="user") # Default is uselist=True (one-to-many)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}')>"
