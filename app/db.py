from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import Config

SQLALCHEMY_DATABASE_URL = Config.db.DATABASE_URL
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=Config.DEBUG)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
