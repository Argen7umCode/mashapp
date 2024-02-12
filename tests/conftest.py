import asyncio
import os
import sys
from typing import Generator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

import os

sys.path[0] = "/".join(os.getcwd().split("/")[:-1])


import config


CLEAN_TABLES = ["users", "mashups", "sources", "authors", "mashup_source_table"]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


engine = create_async_engine(
    config.TEST_DB_PATH,
    future=True,
    echo=True,
)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession, autoflush=True
)


@pytest.fixture(scope="session", autouse=True)
async def _get_test_db() -> Generator:
    session: AsyncSession = async_session()
    try:
        print("SESSION OPEN")
        yield session
    finally:
        print("SESSION CLOSED")
        await session.rollback()
        await session.close()


# async def _get_test_db() -> Generator:
#     try:


#         test_async_session = sessionmaker(
#             test_engine, expire_on_commit=False,
#             class_=AsyncSession,
#             autocommit=False,
#             autoflush=False
#         )
#         yield test_async_session()
#     finally:
#         print('CLOSED SESSION')
#         await
#         test_async_session.close()
