from app.config import settings
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.database.models.entities import Product, StockTransaction
from sqlmodel import SQLModel

engine = create_async_engine(
    url = settings.db_url,
    echo = True
)

async def init_db(engine: AsyncEngine):
    async with engine.begin() as async_engine:
        await async_engine.run_sync(SQLModel.metadata.create_all)

async def close_db(engine: AsyncEngine):
    await engine.dispose()
