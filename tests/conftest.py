import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.main import app
from src.db.build import Base
from src.utils.config.build import config

TEST_DATABASE_URL = config.DATABASE_URL(
    type="asyncpg", 
    hide_password=False,
    override_db="amt_test",
    override_host="localhost",
)
test_engine = create_async_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="session")
def event_loop():
    """Создает один экземпляр цикла событий на всю сессию тестов."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def db_session():
    connection = await test_engine.connect()
    transaction = await connection.begin()
    
    session = AsyncSession(bind=connection, expire_on_commit=False)

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()

# Создание таблиц в бд
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
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
    
                        