from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    message: str

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseModel):
    is_read: bool

class Notification(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
