from sqlalchemy.ext.asyncio import AsyncSession

from typing import Any
import pytest


@pytest.fixture(scope="module")
def prepare_valid_test_user_data() -> dict[str, Any]:
    return {
        "id": None,
        "name": "Artur",
        "username": "argen7um",
        "email": "argen7um@mail.com",
        "hashed_password": "tespass",
        "is_active": True,
    }


@pytest.fixture(scope="module")
def prepare_valid_test_mashup_data() -> dict[str, Any]:
    return {
        "id": None,
        "name": "test_mashup_name",
        "is_active": True,
        "audio": bytes(1),
    }


@pytest.fixture(scope="module")
def prepare_valid_test_source_data() -> dict[str, Any]:
    return {
        "id": None,
        "name": "test_source_name",
        "is_active": True,
        "audio": bytes(1),
    }


@pytest.fixture(scope="module")
def prepare_valid_test_author_data() -> dict[str, Any]:
    return {"id": None, "name": "test_author_name", "is_active": True}
