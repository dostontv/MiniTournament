from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import tournament_router
from app.db import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(tournament_router, prefix="/tournaments", tags=["Tournaments"])
