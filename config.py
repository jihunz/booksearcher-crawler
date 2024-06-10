import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000
    TARGET_URL: str = 'https://www.u-library.kr/'
    PROXY_SOURCE_URL: str = 'https://www.sslproxies.org'

    def get_search_url(self, term: str) -> str:
        return f"https://www.u-library.kr/search/tot/result?st=EXCT&si=TOTAL&q={term}&folder_id=null"


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
