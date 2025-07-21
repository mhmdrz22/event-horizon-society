from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Union

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.token import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.ALGORITHM
JWT_SECRET_KEY = settings.SECRET_KEY

def create_access_token(subject: Union[str, Any], user_id: int, user_role: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "user_id": user_id,
        "user_role": user_role,
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def decode_token(token: str) -> Optional[TokenPayload]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        # Ensure 'sub' is present as per TokenPayload definition in schemas
        if payload.get("sub") is None:
            # Depending on strictness, could raise an error or return None
            # For now, relies on TokenPayload validation during unpacking if 'sub' is not Optional there
            pass
        return TokenPayload(**payload)
    except JWTError:
        return None
