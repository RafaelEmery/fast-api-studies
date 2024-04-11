from pytz import timezone

from typing import Optional
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.user import User
from core.configs import settings
from core.security import verify_password

from pydantic import EmailStr


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="{settings.API_V1_STR}/users/login"
)


async def authenticate(email: EmailStr, password: str, db: AsyncSession) -> Optional[User]:
    async with db() as session:
        result = await session.execute(select(User).filter(User.email == email))
        user: User = result.scalars().unique().one_or_none()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


def _create_token(type: str, expires_delta: timedelta, sub: str) -> str:
    # More info at https://datatracker.ietf.org/doc/html/rfc7519#sectom-4.1.3
    payload = {}
    
    tz = timezone("America/Sao_Paulo")
    expires_at = datetime.now(tz) + expires_delta

    # Defining the token payload
    payload["type"] = type # Token type
    payload["exp"] = expires_at # Exp = expires
    payload["iat"] = datetime.now(tz) # Iat = Issued At
    payload["sub"] = sub # Subject

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(sub: str) -> str:
    """
    More info at https://jwt.io
    """
    return _create_token(
        type="access_token",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), 
        sub=sub
    )