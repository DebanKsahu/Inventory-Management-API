from fastapi import FastAPI
from fastapi_pagination import add_pagination
from contextlib import asynccontextmanager
from psycopg import OperationalError
from sqlmodel import text

from app.database import close_db, init_db, engine
from app.routes.product_routes import product_router
from app.routes.stock_routes import stock_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(engine=engine)
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except OperationalError as e:
        raise RuntimeError("Could not connect to the database") from e
    yield
    await close_db(engine=engine)

app = FastAPI(lifespan=lifespan)
app.include_router(product_router)
app.include_router(stock_router)
add_pagination(app)