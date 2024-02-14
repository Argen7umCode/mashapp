import asyncio
import os
import sys
from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from pytest_asyncio import is_async_test

import os

sys.path[0] = "/".join(os.getcwd().split("/")[:-1])


import config



def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker)





# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="session")
def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


@pytest_asyncio.fixture(scope="function")
async def _get_test_db() -> Generator:
    # session: AsyncSession = async_session()
    engine = create_async_engine(
        config.TEST_DB_PATH,
        future=True,
        echo=True,
    )
    session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession, autoflush=True
    )
    print(session)
    try:
        print("SESSION OPEN")
        async with session() as ses:
            yield ses
    finally:
        await ses.rollback()
        await ses.close()
        print("SESSION CLOSE")





