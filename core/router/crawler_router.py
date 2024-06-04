from datetime import timedelta

from fastapi import APIRouter
from starlette.responses import JSONResponse

from core.service.crawler_service import Crawler_service as service
import traceback
from loguru import logger

from util.log.custom_logger import Custom_logger

router = APIRouter(prefix='/api/crawler', tags=['crawler'])


@router.get("", tags=['get'])
async def crawl():
    try:
        return JSONResponse(await service.crawl())
    except Exception as e:
        logger.error(traceback.format_exc())
        return
