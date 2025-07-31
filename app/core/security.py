from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Union

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session


from app.core.config import settings
from app.schemas.token import TokenPayload


# Explicitly set the schemes to avoid deprecation warnings for the 'crypt' scheme.
# "bcrypt" is the recommended default. "auto" handles deprecation gracefully.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.ALGORITHM
JWT_SECRET_KEY = settings.SECRET_KEY

def create_access_token(
    subject: Union[str, Any],
    user_id: int,
    user_role: str,
    full_name: str,
    is_superuser: bool,
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "user_id": user_id,
        "user_role": user_role,
        "full_name": full_name,
        "is_superuser": is_superuser,
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


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")

from app.db.session import get_db
from app.models.user import User

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None or payload.sub is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == payload.sub).first()
    if user is None:
        raise credentials_exception
    return user
