import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool 

from src.main import app
from src.db.build import Base
from src.utils.config.build import config

@pytest_asyncio.fixture()
async def engine():
    """Создает движок БД внутри активного цикла событий."""
    # Получаем URL из конфига (как ты делал раньше)
    db_host = config.POSTGRES_HOST if os.getenv("IN_DOCKER") == "1" else "localhost"
    url = config.DATABASE_URL(
        type="asyncpg", 
        hide_password=False,
        override_db="amt_test",
        override_host=db_host,
    )
    _engine = create_async_engine(url, echo=False, poolclass=NullPool)
    yield _engine
    await _engine.dispose()

@pytest_asyncio.fixture
async def db_session(engine):
    connection = await engine.connect()
    transaction = await connection.begin()
    
    session = AsyncSession(bind=connection, expire_on_commit=False)

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()

# Создание таблиц в бд
@pytest_asyncio.fixture(autouse=True)
async def setup_db(engine):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)   # Удаляем старое
        await conn.run_sync(Base.metadata.create_all) # Создаем чистое
    yield
    # async with test_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

# Настройка подмены сессии
@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    from src.db.build import get_async_db
    async def _override_get_async_db():
        yield db_session

    app.dependency_overrides[get_async_db] = _override_get_async_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

# Проверка подмены
@pytest_asyncio.fixture(autouse=True)
def check_overrides(client):
    from src.db.build import get_async_db
    if get_async_db not in app.dependency_overrides:
        pytest.fail(f"Dependency {get_async_db} is not overridden!")
    
                        