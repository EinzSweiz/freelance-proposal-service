from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5436/proposals_db")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

class Base(DeclarativeBase):
    pass
