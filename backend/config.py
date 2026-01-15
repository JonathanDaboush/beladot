import os
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    ENV: str = 'development'
    DEBUG: bool = False
    DATABASE_URL: str
    LOG_LEVEL: str = 'INFO'
    SECRET_KEY: str = 'changeme'
    # Add more config as needed

    model_config = {
        'env_file': '.env',
        'env_file_encoding': 'utf-8',
        'extra': 'allow',
    }

settings = Settings()
