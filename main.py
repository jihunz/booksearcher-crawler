import logging

from fastapi import FastAPI
# from analysis.router import analysis_router
import uvicorn

from util.log.custom_logger import Custom_logger
from config import get_config

# 설정 로드
config = get_config()

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title='CustomLogger', debug=False)
    app.logger = Custom_logger.create()

    return app


app = create_app()

# app.include_router(analysis_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.APP_HOST, port=config.APP_PORT)
