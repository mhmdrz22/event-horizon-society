import enum
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as DBEnum, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import CustomBase as Base

class NewsStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"

class News(Base):
    __tablename__ = "news" # Explicitly "news", Base would default to "newss"

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(DBEnum(NewsStatus), default=NewsStatus.DRAFT, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="news_items")

    # Relationships


    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', status='{self.status.value}')>"
