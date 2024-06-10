from fastapi import FastAPI
import uvicorn

from core.router import crawler_router
from util.log.custom_logger import Custom_logger
from config import get_config

# 설정 로드
config = get_config()

# 로거 설정
logger = Custom_logger.create()


def create_app() -> FastAPI:
    app = FastAPI(title="CustomLogger", debug=False)

    # 커스텀 로거를 FastAPI 로거로 설정
    app.logger = logger

    # 라우터 추가
    app.include_router(crawler_router.router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.APP_HOST, port=config.APP_PORT, log_config=None)
