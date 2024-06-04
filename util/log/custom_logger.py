import logging
import os
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class Custom_logger:
    @classmethod
    def create(cls):
        logger.remove()
        log_file_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logfile')

        # 로깅을 파일로 저장 -> 00:00에 초기화, 10일 동안 파일로 보관, 보관 후 zip으로 압축
        logger.add(
            str(os.path.join(log_file_dir_path, '{time:YYYY-MM-DD}.log')),
            rotation="00:00",
            retention="10 days",
            compression="zip",
            encoding="utf-8",
            level="INFO",
            backtrace=False,
            diagnose=False,
            enqueue=True,
            format="<level>{level: <8}</level>| <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        )

        logger.add(
            sys.stdout,
            # format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            format="<level>{level: <8}</level>| <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
            level="INFO",
            backtrace=False,
            diagnose=False,
            enqueue=True
        )

        logging.basicConfig(handlers=[InterceptHandler()], level=logging.ERROR)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn', 'uvicorn.error', 'fastapi']:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]
        logger.bind(request_id=None, method=None)

        return logger

    @classmethod
    def custom_err(cls, str):
        msg = {
            "status": "error",
            "message": str
        }
        logger.error(msg)
        return msg


    @classmethod
    def val_exception(cls, str):
        logger.error({
            "status": "error",
            "message": str
        })
        raise ValueError(str)
