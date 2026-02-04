from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.sql import Base
from app.models.nosql import InferenceLog

# 1. SQLAlchemy Setup
engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_sql_db():
    # In dev, we can auto-create tables. In prod, use Alembic.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 2. MongoDB/Beanie Setup
async def init_mongo_db():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(database=client[settings.MONGO_DB_NAME], document_models=[InferenceLog])
