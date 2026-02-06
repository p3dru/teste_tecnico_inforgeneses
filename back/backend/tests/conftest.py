import os
import pytest
import pytest_asyncio
import tempfile
import shutil
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

# Set test environment variables BEFORE importing app modules
_test_shared_dir = "/tmp/test-shared-data-pytest"
_test_uploads_dir = os.path.join(_test_shared_dir, "uploads")
os.makedirs(_test_uploads_dir, exist_ok=True)

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("MONGO_URL", "mongodb://test:test@localhost:27017")
os.environ.setdefault("KESTRA_USER", "test")
os.environ.setdefault("KESTRA_PASSWORD", "test")
os.environ.setdefault("KESTRA_URL", "http://localhost:8080")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000")
os.environ.setdefault("SHARED_UPLOADS_DIR", _test_uploads_dir)  # Override for tests

from app.main import app
from app.db.session import get_db, Base
from app.models.sql import User
from app.core import security
from app.api.deps import get_current_user

# Create temporary SQLite file for tests (more robust than :memory:)
_test_db_file = os.path.join(tempfile.gettempdir(), "test_wildfire.db")
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{_test_db_file}"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database():
    """
    Create database tables once for the entire test session.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    # Cleanup database file
    if os.path.exists(_test_db_file):
        os.remove(_test_db_file)


@pytest_asyncio.fixture(scope="function")
async def db_session(setup_test_database) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database session for each test.
    Uses savepoint/rollback for test isolation.
    """
    connection = await test_engine.connect()
    transaction = await connection.begin()
    
    session = AsyncSession(bind=connection, expire_on_commit=False)
    
    yield session
    
    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client with overridden dependencies.
    """
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> User:
    """
    Create a test user in the database.
    """
    user = User(
        username="testuser",
        hashed_password=security.get_password_hash("testpass123"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_headers(test_user: User) -> dict:
    """
    Generate authentication headers for the test user.
    """
    access_token = security.create_access_token(subject=test_user.username)
    return {"Authorization": f"Bearer {access_token}"}


@pytest_asyncio.fixture
async def authenticated_client(
    client: AsyncClient, 
    test_user: User, 
    auth_headers: dict,
    db_session: AsyncSession
) -> AsyncGenerator[AsyncClient, None]:
    """
    Client with authentication pre-configured.
    """
    # Override get_current_user to return test_user directly
    async def override_get_current_user():
        return test_user
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    # Set headers on client
    client.headers.update(auth_headers)
    
    yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
def mock_kestra_trigger(monkeypatch):
    """
    Mock the Kestra client to avoid real HTTP calls.
    """
    def mock_trigger(file_path: str, report_id: str):
        return f"mock-execution-{report_id}"
    
    monkeypatch.setattr("app.core.kestra_client.trigger_fire_detection_flow", mock_trigger)
    return mock_trigger


def pytest_sessionfinish(session, exitstatus):
    """Cleanup temp directory after all tests."""
    if os.path.exists(_test_shared_dir):
        shutil.rmtree(_test_shared_dir, ignore_errors=True)
