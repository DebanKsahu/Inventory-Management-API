from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database import engine


class DatabaseDependency():

    async_session_factory = async_sessionmaker(bind=engine)

    @staticmethod
    async def get_session():
        async with DatabaseDependency.async_session_factory() as session:
            yield session

class DependencyContainer(
    DatabaseDependency
):
    pass