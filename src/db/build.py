import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.utils.config.build import config
from src.db.sql_obj import ReprMixin, SqlTypes
from src.db.exc import (
    BuildDataBaseCoreError, CreateAllDataBaseError
)

logger = logging.getLogger(__name__)

class Base(DeclarativeBase, ReprMixin):
    type_annotation_map = SqlTypes.type_annotation_map
    ...

class DataBaseCore:
    def __init__(self):
        try:
            self.config=config
            self.metadata = Base.metadata
            self.sync_engine = self.__create_sync_engine()
            self.async_engine = self.__create_async_engine()
            self.session_factory = sessionmaker(self.sync_engine)
            self.async_session_factory = async_sessionmaker(self.async_engine, expire_on_commit=False)
            # self.__init_models()
            # logger.debug(f"{self.sync_engine.get_execution_options()}")
            # logger.debug(f"{self.async_engine.get_execution_options()}")
        except Exception as e:
            msg = (
                "Не удалось инициализировать DataBaseCore!\n"
                f"Детали:\n{e}"
            )
            raise BuildDataBaseCoreError(msg)

    def create_all_tables(self):
        try:
            self.metadata.create_all(self.sync_engine)
        except Exception as e:
            msg = (
                "Не удалось инициализировать БД!\n"
                f"Детали:\n{e}"
            )
            raise CreateAllDataBaseError(msg)

    def get_db_url(self, type: str, **kwargs):
        """
        Формирует URL.
        """
        url = self.config.DATABASE_URL(
            type=type, 
            hide_password=False,
            **kwargs,
        )
        return url

    def __create_sync_engine(self):
        current_schema = config.POSTGRES_SCHEMA
        sync_engine = create_engine(
            url=self.get_db_url("psycopg"),
            # echo=ECHO_MODE,
            pool_size=5,
            # max_overflow=10,
            hide_parameters=True,
            execution_options={
                "schema_translate_map": {None: current_schema},
            }
        )
        return sync_engine
    def __create_async_engine(self):
        current_schema = config.POSTGRES_SCHEMA
        async_engine = create_async_engine(
            url=self.get_db_url("asyncpg"),
            # echo=ECHO_MODE,
            hide_parameters=True,
            execution_options={
                "schema_translate_map": {None: current_schema},
            }
        )
        return async_engine
    
    def get_sync_db(self):
        session = self.session_factory()
        try:
            yield session
        finally:
            session.close()

    async def get_async_db(self):
        async with self.async_session_factory() as session:
            yield session

    def __init_models(self):
        from src.db.models import Plug

        logger.info("init models success")

    def init_models(self):
        self.__init_models()

    async def dispose(self):
            """Явное закрытие всех ресурсов базы данных"""
            logger.info("Закрытие соединений базы данных...")
            if self.async_engine:
                await self.async_engine.dispose()
            if self.sync_engine:
                self.sync_engine.dispose()

databasecore = DataBaseCore()

async def get_async_db():
    async for session in databasecore.get_async_db():
        yield session
        