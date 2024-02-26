from typing import Generator, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session


async def get_session() -> AsyncGenerator[Generator, None]:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()

