from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import CustomBase as Base

class EventRegistration(Base):
    __tablename__ = "event_registrations"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="event_registrations")
    event = relationship("Event", back_populates="registrations")

    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='uq_user_event_registration'),
    )

    def __repr__(self):
        return f"<EventRegistration(id={self.id}, user_id={self.user_id}, event_id={self.event_id})>"
