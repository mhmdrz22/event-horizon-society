from sqlalchemy import Column, String, Text, DateTime, Time, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Event(Base):
    __tablename__ = "events"

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    # Sticking with DateTime for the event's start datetime as decided in the prompt block.
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

    # __table_args__ below will have the constraints.
    # This comment block can be removed or used for other relationship placeholders if any.

    __table_args__ = (
        CheckConstraint('registered_count <= capacity', name='cc_registered_count_less_than_equal_capacity'),
        CheckConstraint('capacity > 0', name='cc_capacity_positive'),
        CheckConstraint('registered_count >= 0', name='cc_registered_count_non_negative'),
    )

    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}', date='{self.event_datetime}')>"
