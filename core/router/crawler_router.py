from fastapi import APIRouter, Query
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from core.service.crawler_service import Crawler_service as service
import traceback
from loguru import logger

router = APIRouter(prefix='/api/crawler', tags=['crawler_router'])


@router.get("", tags=['crawler_router'])
async def crawl(term: str = Query):
    try:
        result = await service.exec_crawl(term)
        return JSONResponse(result)
    except Exception as e:
        logger.error(traceback.format_exc())
        return
