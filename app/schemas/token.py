from pydantic import BaseModel
from typing import Optional
from .user import User  # Import the User schema

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User  # Add user field

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    user_id: Optional[int] = None
    user_role: Optional[str] = None
    full_name: Optional[str] = None
