import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Импорт для CORS

from src.api.exc import AddMiddlewareError, SetupMiddlewareUrlsError
from src.utils.config.build import config

logger = logging.getLogger(__name__)

class Middleware:
    @staticmethod
    def setup_urls():
        try:
            urls = []
            urls.append(f"http://localhost:{config.API_PORT}")
            logger.debug("SetupMiddlewareUrls success")
            return urls
        except Exception as e:
            msg = (
                "Не удалось собрать urls!\n"
                f"Детали:\n{e}"
            )
            raise SetupMiddlewareUrlsError(msg)        

    @staticmethod
    def add_middleware(app:FastAPI):
        try:
            urls=Middleware.setup_urls()
            app.add_middleware(
                CORSMiddleware,
                allow_origins=[urls],
                allow_credentials=True,
                allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
                allow_headers=["*"],  # Разрешить все заголовки
            )
            logger.info("FastApi Middleware success")
        except Exception as e:
            msg = (
                "Не удалось настроить middleware!\n"
                f"Детали:\n{e}"
            )
            raise AddMiddlewareError(msg)
