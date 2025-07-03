from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None # 'sub' is standard for subject (user identifier, e.g. email or id)
    # Add any other data you want to store in the token, e.g. scopes, roles
    # For example:
    # user_id: Optional[int] = None
    # role: Optional[str] = None
