from sqlalchemy import Column, Text, DateTime, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import CustomBase as Base

class Comment(Base):
    __tablename__ = "comments"

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

    def __repr__(self):
        target_info = ""
        if self.news_id:
            target_info = f"news_id={self.news_id}"
        elif self.event_id:
            target_info = f"event_id={self.event_id}"
        return f"<Comment(id={self.id}, user_id={self.user_id}, {target_info})>"
