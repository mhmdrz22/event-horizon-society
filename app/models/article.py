import enum
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as DBEnum, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import CustomBase as Base

class ArticleStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Article(Base):
    __tablename__ = "articles"

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    status = Column(DBEnum(ArticleStatus), default=ArticleStatus.PENDING, nullable=False)
    review_comments = Column(Text, nullable=True)

    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True) # Nullable, as it's set upon review

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # author = relationship("User", back_populates="articles")

    # Relationships (e.g., if articles can have comments too, though not explicitly in this model's plan)
    # comments = relationship("Comment", back_populates="article_item", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}', status='{self.status.value}')>"
