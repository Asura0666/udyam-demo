# # conftest.py
# import os
# from typing import AsyncGenerator
# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from alembic import command
# from alembic.config import Config as AlembicConfig
# from src.main import app # Import the main app instance
# from src.db.main import get_session
# from src.config import Config
# import pytest_asyncio
# from sqlmodel import SQLModel
# from httpx import AsyncClient, ASGITransport


# DB_URL = Config.TEST_DATABASE_URL

# test_engine = create_async_engine(
#     url=DB_URL,
#     echo=True
# )

# #create a session to override the default db session
# async def test_get_session() -> AsyncGenerator[AsyncSession, None]:
#     Session = sessionmaker(class_=AsyncSession, expire_on_commit=False)
#     try:
#         async with Session(bind=test_engine) as session:
#             yield session
#     finally:
#         await session.close()

# @pytest_asyncio.fixture(scope="session")
# async def test_client():
#     async with test_engine.begin() as conn:
#         from src.db.models import UdyamApplication, VerificationAttempt
#         await conn.run_sync(SQLModel.metadata.create_all)

#     # override the session
#     app.dependency_overrides[get_session] = test_get_session

#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         yield client

# ------------------------------------------------------------------

# # conftest.py
# import os
# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from alembic import command
# from alembic.config import Config as AlembicConfig
# from src import app
# from src.db.main import get_session

# # -----------------
# # Set test env vars before imports
# # -----------------
# os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
# os.environ["POSTGRES_USER"] = "test"
# os.environ["POSTGRES_PASSWORD"] = "test"
# os.environ["POSTGRES_DB"] = "test"

# DATABASE_URL = os.environ["DATABASE_URL"]
# async_engine = create_async_engine(DATABASE_URL, future=True)

# # Override the DB dependency
# async def override_get_session() -> AsyncSession:
#     async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
#     async with async_session() as session:
#         yield session

# app.dependency_overrides[get_session] = override_get_session
# client = TestClient(app)

# # -----------------
# # Alembic helpers
# # -----------------
# def run_migrations_online():
#     alembic_cfg = AlembicConfig("alembic.ini")
#     alembic_cfg.set_main_option("script_location", "alembic")  # migrations folder
#     alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
#     command.upgrade(alembic_cfg, "head")

# def rollback_migrations():
#     alembic_cfg = AlembicConfig("alembic.ini")
#     alembic_cfg.set_main_option("script_location", "alembic")
#     alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
#     command.downgrade(alembic_cfg, "base")

# # -----------------
# # Fixtures
# # -----------------
# @pytest.fixture(scope="session", autouse=True)
# def prepare_database():
#     run_migrations_online()
#     yield
#     rollback_migrations()

# @pytest.fixture
# def test_client():
#     return client

# ------------------------------------------------------------------

# conftest.py
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from src import app
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest
import uuid
from datetime import date


from src.db.main import get_session

DB_URL = Config.TEST_DATABASE_URL

test_engine = create_async_engine(url=DB_URL, echo=True)


# Async session override for tests
async def test_get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(class_=AsyncSession, expire_on_commit=False)
    try:
        async with Session(bind=test_engine) as session:
            yield session
    finally:
        await session.close()


@pytest.fixture(scope="session")
def test_client():
    """Create all tables and return a sync TestClient."""
    import asyncio

    async def init_models():
        async with test_engine.begin() as conn:
            from src.db.models import UdyamApplication, VerificationAttempt

            await conn.run_sync(SQLModel.metadata.create_all)

    asyncio.run(init_models())

    # Override the session dependency
    app.dependency_overrides[get_session] = test_get_session

    with TestClient(app) as client:
        yield client


@pytest.fixture()
def aadhaar_payload():
    return {
        "aadhaarNumber": "123412341234",
        "entrepreneurName": "John Doe",
        "consent": True,
    }


@pytest.fixture()
def otp_verify_payload():
    return {
        "app_id": "app123",
        "transaction_id": "txn456",
        "otp": "123456",
    }


@pytest.fixture()
def pan_payload():
    return {
        "appId": str(uuid.uuid4()),
        "panNumber": "ABCDE1234F",
        "panHolderName": "Jane Doe",
        "dobOrDoi": date(1990, 1, 1).isoformat(),
        "consent": True,
    }


@pytest.fixture()
def final_form_payload():
    return {
        "entrepreneurName": "John Doe",
        "typeOfOrganisation": "Partnership",
        "dobOrDoi": "01-01-1990",  # tests dd-mm-yyyy parsing
        "previousYearITR": "1",  # YES
        "hasGSTIN": "2",  # NO
    }
