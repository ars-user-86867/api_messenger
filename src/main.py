import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.utils.config.build import config
from src.api.utils.middleware import Middleware
from src.api.routers.build import main_router
# from src.api.exc import add_jwt_exceptions
from src.db.build import databasecore
from src.utils.logs.build import BaseLogger
BaseLogger.setup_logger()

logger = logging.getLogger(__name__)

def setup_middleware(app: FastAPI):
    Middleware.add_middleware(app)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.config = config
    app.state.databasecore = databasecore
    databasecore.init_models()
    # теперь alembic
    # databasecore.create_all_tables()
    logger.info("приложение запущено")
    yield
    logger.warning("приложение остановлено")
    # await _tbot.stop_tbot()
    await databasecore.dispose()
    # BuildLogger.end_logger_listener_process(queue,listener)

def create_app() -> FastAPI:
    app=FastAPI(lifespan=lifespan)
    setup_middleware(app)
    app.include_router(main_router)
    # add_jwt_exceptions(app)
    return app
    
app=create_app()

if __name__=="__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001, 
        log_level="debug", 
        reload=True
    )
