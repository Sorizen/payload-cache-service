from collections.abc import AsyncIterator, Iterator

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from testcontainers.community.postgres import PostgresContainer

from app.database import get_db
from app.dependencies import get_transformer
from main import app
from tests.fakes import CountingTransformer

POSTGRES_IMAGE = 'postgres:17-alpine'
POSTGRES_DRIVER = 'asyncpg'
TABLES = ('payloads', 'transformations')


@pytest.fixture(scope='session')
def database_url() -> Iterator[str]:
    with PostgresContainer(POSTGRES_IMAGE, driver=POSTGRES_DRIVER) as postgres:
        url = postgres.get_connection_url()
        config = Config('alembic.ini')
        config.set_main_option('sqlalchemy.url', url)
        command.upgrade(config, 'head')
        yield url


@pytest.fixture(scope='session')
async def engine(database_url: str) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(database_url, poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest.fixture(autouse=True)
async def clean_tables(engine: AsyncEngine) -> AsyncIterator[None]:
    yield
    async with engine.begin() as connection:
        await connection.execute(text(f'TRUNCATE {", ".join(TABLES)}'))


@pytest.fixture
def transformer() -> CountingTransformer:
    return CountingTransformer()


@pytest.fixture
async def client(
    engine: AsyncEngine, transformer: CountingTransformer
) -> AsyncIterator[AsyncClient]:
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with session_factory() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_transformer] = lambda: transformer
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client
    app.dependency_overrides.clear()
