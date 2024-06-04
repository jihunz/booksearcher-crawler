import traceback

from loguru import logger


class Crawler_service:

    @classmethod
    async def crawl(cls):
        try:
            return ""
        except Exception as e:
            logger.error(traceback.format_exc())
            return
