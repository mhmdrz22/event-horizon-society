from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.membership_request import MembershipRequestStatus as ModelMembershipRequestStatus # Enum
from .user import User # For embedding user information

class MembershipRequestBase(BaseModel):
    # user_id will be set from authenticated user
    # requested_at will be set by the server
    pass

class MembershipRequestCreate(MembershipRequestBase):
    # No specific fields needed from user for creation if it's just a "request" action
    pass

class MembershipRequestUpdate(BaseModel): # For admin review
    status: ModelMembershipRequestStatus

class MembershipRequest(BaseModel):
    id: int
    user_id: int
    status: ModelMembershipRequestStatus
    requested_at: datetime
    reviewed_at: Optional[datetime] = None
    user: Optional[User] = None # Embed user details

    # Pydantic V2 compatibility
    model_config = {"from_attributes": True}
