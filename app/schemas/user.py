from pydantic import BaseModel, EmailStr, constr, model_validator
from typing import Optional
from datetime import datetime
# Attempt to import UserRole from models. This is a common pattern.
from app.models.user import UserRole as ModelUserRole # Alias to avoid Pydantic confusion with a potential UserRole schema

class UserBase(BaseModel):
    email: EmailStr
    full_name: constr(min_length=1, max_length=255)
    phone_number: Optional[constr(max_length=20)] = None # Add validation regex later if needed
    is_superuser: bool = False

class UserCreate(UserBase):
    password: constr(min_length=8)
    student_id: Optional[constr(min_length=1, max_length=50)] = None # Made optional
    role: ModelUserRole = ModelUserRole.STUDENT
    is_superuser: bool = False

    @model_validator(mode='before')
    @classmethod
    def check_student_id_for_student_role(cls, values):
        """Ensure student_id is provided if the role is STUDENT."""
        # This validator is defined with pre=True, so it runs on the raw dict before model creation
        role = values.get('role', ModelUserRole.STUDENT) # Default to student if not provided
        student_id = values.get('student_id')
        if role == ModelUserRole.STUDENT and not student_id:
            raise ValueError('student_id is required for users with the STUDENT role')

        # If the role is not student, we can even ensure student_id is not set
        if role != ModelUserRole.STUDENT and student_id is not None:
            # Depending on strictness, you could clear it or raise an error.
            # For now, let's just allow it but it won't be used.
            pass

        return values

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel): # UserBase makes all fields required by default, for update better to be explicit
    email: Optional[EmailStr] = None
    full_name: Optional[constr(min_length=1, max_length=255)] = None
    student_id: Optional[constr(max_length=50)] = None
    phone_number: Optional[constr(max_length=20)] = None
    password: Optional[constr(min_length=8)] = None
    role: Optional[ModelUserRole] = None # Allow role update for admins
    is_superuser: Optional[bool] = None

# Properties to return to client
class User(UserBase):
    id: int
    role: ModelUserRole # Use the aliased model enum
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# Properties stored in DB (internal representation, not for direct API output)
class UserInDB(UserBase): # Renamed from UserInDB to UserInDBBase to avoid confusion with User schema above
    id: int
    role: ModelUserRole
    created_at: datetime
    updated_at: datetime
    password_hash: str

    model_config = {"from_attributes": True}

class UserStatusUpdate(BaseModel):
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

