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
    pass

class TestSettings(BaseAppSettings):
    # Provide safe defaults for tests to allow import/run without external env
    SECRET_KEY: str = 'test-secret-key'
    EMAIL_API_KEY: str = 'test-email-api-key'
    DATABASE_URL: str = 'sqlite:///./test.db'
    # For tests, ignore extra env vars and avoid loading .env
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding='utf-8',
        extra='ignore',
        frozen=True,
    )

class ProductionSettings(BaseAppSettings):
    pass

def _load_settings() -> BaseAppSettings:
    # Peek ENV from environment to select settings class
    env = os.environ.get('ENV')
    if env is None:
        # Fail fast: explicit ENV required
        raise RuntimeError('ENV environment variable is required')
    env = env.strip().lower()
    if env == 'dev':
        return DevelopmentSettings()
    if env == 'test':
        return TestSettings()
    if env == 'prod':
        return ProductionSettings()
    raise RuntimeError("ENV must be one of 'dev', 'test', 'prod'")

settings = _load_settings()
