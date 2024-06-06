import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000


class DevelopmentConfig(Config):
    APP_PORT: int = 2024


class ProductionConfig(Config):
    APP_PORT: int = 2024


def get_config():
    env = os.getenv("ENV", "prod")
    config_type = {
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig()
    }
    return config_type[env]


config: Config = get_config()
