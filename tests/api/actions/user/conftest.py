from sqlalchemy.ext.asyncio import AsyncSession

from typing import Any
import pytest


@pytest.fixture(scope="module")
def prepare_valid_test_data() -> dict[str, Any]:
    return {
        "id": None,
        "name": "Artur",
        "username": "argen7um",
        "email": "argen7um@mail.com",
        "hashed_password": "tespass",
        "is_active": True,
    }
