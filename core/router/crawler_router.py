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
        result = await service.crawl(term)
        for item in result:
            print(item)

        # json_response = jsonable_encoder(result)
        # print(json_response)
        # return JSONResponse(content=json_response)
    except Exception as e:
        logger.error(traceback.format_exc())
        return
