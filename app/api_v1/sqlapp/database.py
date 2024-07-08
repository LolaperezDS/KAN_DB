from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from api_v1.sqlapp.config import DB_NAME, DB_PASS, DB_USER, DB_PORT, DB_HOST
from asyncio import current_task


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL)
session_factory = sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession
        )

def get_scoped_session():
        session = scoped_session(session_factory=session_factory,
                                       scopefunc=current_task)
        return session

async def session_dependency() -> AsyncSession:
    session = get_scoped_session()
    yield session
    await session.remove()

Base = declarative_base()