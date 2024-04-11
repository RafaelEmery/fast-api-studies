from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.configs import settings
from core.auth import oauth2_schema
from core.database import Session
from models.user import User

class Token(BaseModel):
    user_id: Optional[str] = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session
    """
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()


async def get_current_user(
    token: str = Depends(oauth2_schema), 
    db: AsyncSession = Depends(get_session)
) -> User:
    """
    Get current authenticated user from bearer token
    """
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}, # Authentication method
    )
    try:
        # Deconding token
        payload = jwt.decode(
            token, settings.JWT_SECRET, 
            algorithms=[settings.ALGORITHM], 
            options={"verify_aud": False}
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credential_exception
        
        token_data: Token = Token(user_id=user_id)
    except JWTError:
        raise credential_exception
    
    # Getting current user on database
    async with db() as session:
            result = await session.execute(select(User).filter(User.id == int(token_data.user_id)))
            user: User = result.scalars().unique().one_or_none()
            if not user:
                raise credential_exception
            return user
