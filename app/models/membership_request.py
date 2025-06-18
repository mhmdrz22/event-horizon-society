import enum
from sqlalchemy import Column, DateTime, ForeignKey, Enum as DBEnum, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class MembershipRequestStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class MembershipRequest(Base):
    __tablename__ = "membership_requests"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True) # Added index=True for user_id
    status = Column(DBEnum(MembershipRequestStatus), default=MembershipRequestStatus.PENDING, nullable=False)

    requested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True) # Nullable, as it's set upon review

    # For a one-to-many relationship (User has many MembershipRequests)
    user = relationship("User", back_populates="membership_requests")

    # If we wanted to enforce one active PENDING request per user, we'd add a UniqueConstraint here,
    # typically on (user_id, status) with a condition for status='pending'.
    # e.g. __table_args__ = (UniqueConstraint('user_id', 'status', name='uq_user_pending_request', postgresql_where=status=='pending'),)
    # For now, keeping it simple as per prompt, no such constraint.

    def __repr__(self):
        return f"<MembershipRequest(id={self.id}, user_id={self.user_id}, status='{self.status.value}')>"
