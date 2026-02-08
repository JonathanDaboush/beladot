import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal





from typing import Literal

EnvLiteral = Literal['dev', 'test', 'prod']

class BaseAppSettings(BaseSettings):
    ENV: EnvLiteral
    DATABASE_URL: str
    LOG_LEVEL: str = 'INFO'
    SECRET_KEY: str
    EMAIL_API_KEY: str

    # Pydantic v2 settings configuration
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='forbid',
        frozen=True,
    )

class DevelopmentSettings(BaseAppSettings):
    ENV: EnvLiteral = 'dev'
    # Provide safe, permissive defaults for local development
    # For live server via docker-compose, use divina_dev database
    SECRET_KEY: str = 'dev-secret-key'
    EMAIL_API_KEY: str = 'dev-email-api-key'
    DATABASE_URL: str = 'postgresql+asyncpg://postgres:password@localhost:5432/divina_dev'
    # In dev, do not load general .env and use a DEV_ prefix to avoid accidental overrides
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='DEV_',
        frozen=True,
    )

class TestSettings(BaseAppSettings):
    ENV: EnvLiteral = 'test'
    # Provide safe defaults for tests to allow import/run without external env
    SECRET_KEY: str = 'test-secret-key'
    EMAIL_API_KEY: str = 'test-email-api-key'
    # Use divina_test database for Postgres-based tests
    # Tests use SQLite in-memory by default (see conftest.py)
    # Set TEST_DATABASE_URL to use this Postgres test database instead
    DATABASE_URL: str = 'postgresql+asyncpg://postgres:password@localhost:5432/divina_test'
    # For tests, ignore extra env vars and avoid loading .env
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding='utf-8',
        extra='ignore',
        # Use a dummy prefix so normal env vars (e.g., DATABASE_URL) don't override test defaults
        env_prefix='IGNORE_',
        frozen=True,
    )

class ProductionSettings(BaseAppSettings):
    ENV: EnvLiteral = 'prod'
    pass

def _load_settings() -> BaseAppSettings:
    # Peek ENV from environment to select settings class, default to 'dev'
    env = os.environ.get('ENV')
    # If running under pytest, prefer test settings to avoid requiring Postgres
    if env is None and ('PYTEST_CURRENT_TEST' in os.environ or 'PYTEST_ADDOPTS' in os.environ):
        env = 'test'
    if env is None:
        env = 'dev'
    env = env.strip().lower()
    if env == 'dev':
        return DevelopmentSettings()
    if env == 'test':
        return TestSettings()
    if env == 'prod':
        return ProductionSettings(
            DATABASE_URL='postgresql+asyncpg://postgres:correct_password@localhost:5432/divina_dev',
            SECRET_KEY='prod-secret-key',
            EMAIL_API_KEY='prod-email-key'
        )
    raise RuntimeError("ENV must be one of 'dev', 'test', 'prod'")

settings = _load_settings()
