import os


DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1:5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

DB_PATH = "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
    DB_USER=DB_USER,
    DB_PASSWORD=DB_PASSWORD,
    DB_HOST=DB_HOST,
    DB_NAME=DB_NAME,
)

TEST_DB_USER = os.getenv("DB_USER", "postgres_test")
TEST_DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres_test")
TEST_DB_HOST = os.getenv("DB_HOST", "127.0.0.1:5430")
TEST_DB_NAME = os.getenv("DB_NAME", "postgres_test")

TEST_DB_PATH = (
    "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
        DB_USER=TEST_DB_USER,
        DB_PASSWORD=TEST_DB_PASSWORD,
        DB_HOST=TEST_DB_HOST,
        DB_NAME=TEST_DB_NAME,
    )
)
