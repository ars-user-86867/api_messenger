import logging
from fastapi import APIRouter

from src.api.exc import SetupFastApiRoutes
from src.api.routers.chats.build import router as chats_router

logger = logging.getLogger(__name__)

def build_routes():
    try:
        main_router = APIRouter()
        main_router.include_router(chats_router, tags=["chats"])
        logger.info("build api routes success")
        return main_router
    except Exception as e:
        msg = (
            "Не удалось подключить роутеры!\n"
            f"Детали:\n{e}"
        )
        raise SetupFastApiRoutes(msg)

main_router = build_routes()
