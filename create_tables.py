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
