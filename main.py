import asyncio
import concurrent.futures
import logging
from fastapi import FastAPI, BackgroundTasks
import uvicorn

from core.router import crawler_router
from util.log.custom_logger import Custom_logger
from config import get_config
from util.proxy_manager import Proxy_manager

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


async def run_get_proxy():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, Proxy_manager.get_proxy)

async def run_chk_proxy():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, Proxy_manager.chk_proxy_without_return())


@app.on_event("startup")
async def find_available_proxy():
    background_tasks = BackgroundTasks()
    background_tasks.add_task(asyncio.create_task(run_get_proxy()))
    # background_tasks.add_task(asyncio.create_task(run_chk_proxy()))


if __name__ == "__main__":
    uvicorn.run("main:app", host=config.APP_HOST, port=config.APP_PORT, log_config=None)
