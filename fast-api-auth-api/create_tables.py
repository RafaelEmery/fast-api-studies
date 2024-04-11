from core.configs import settings
from core.configs import engine


async def create_tables() -> None:
    import models.__all
    print("Creating tables")

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    
    print("Tables created")


# If it's running directly (not imported in a module), run the function
if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())