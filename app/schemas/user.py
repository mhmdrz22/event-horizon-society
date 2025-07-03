from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime
# Attempt to import UserRole from models. This is a common pattern.
from app.models.user import UserRole as ModelUserRole # Alias to avoid Pydantic confusion with a potential UserRole schema

class UserBase(BaseModel):
    email: EmailStr
    full_name: constr(min_length=1, max_length=255)
    student_id: Optional[constr(max_length=50)] = None
    phone_number: Optional[constr(max_length=20)] = None # Add validation regex later if needed

class UserCreate(UserBase):
    password: constr(min_length=8) # Basic length validation for password

class UserUpdate(BaseModel): # UserBase makes all fields required by default, for update better to be explicit
    email: Optional[EmailStr] = None
    full_name: Optional[constr(min_length=1, max_length=255)] = None
    student_id: Optional[constr(max_length=50)] = None
    phone_number: Optional[constr(max_length=20)] = None
    password: Optional[constr(min_length=8)] = None
    role: Optional[ModelUserRole] = None # Allow role update for admins

# Properties to return to client
class User(UserBase):
    id: int
    role: ModelUserRole # Use the aliased model enum
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# Properties stored in DB (internal representation, not for direct API output)
class UserInDBBase(UserBase): # Renamed from UserInDB to UserInDBBase to avoid confusion with User schema above
    id: int
    role: ModelUserRole
    created_at: datetime
    updated_at: datetime
    password_hash: str

    model_config = {"from_attributes": True}

# This UserInDB can be used if you need to pass the full UserInDBBase object around
# For example, when fetching from DB and using it internally.
class UserInDB(UserInDBBase):
    pass
