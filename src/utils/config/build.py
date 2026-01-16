import os
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import (
    BaseSettings, SettingsConfigDict
)
from sqlalchemy import URL
from src.utils.config.exc import BuildConfigError

class EnvPathBuilder:
    path = Path("envs")
    file = Path(".env")
    
    @classmethod
    def get_path(cls) -> Path:
        path = (
            cls.path/
            Path(f"{cls.file}")
        )
        return path

# =======================================================
# db
class DbEnvNames:
    POSTGRES_HOST: str = "POSTGRES_HOST"
    POSTGRES_PORT: str = "POSTGRES_PORT"
    POSTGRES_USER: str = "POSTGRES_USER"
    POSTGRES_PASSWORD: str = "POSTGRES_PASSWORD"
    POSTGRES_DB: str = "POSTGRES_DB"
    DBMS: str = "DBMS"
    POSTGRES_SCHEMA: str = "POSTGRES_SCHEMA"

class DbConfig(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_SCHEMA: str
    DBMS: str # Database Management System

    # @classmethod
    def DATABASE_URL(self, 
        type: str = "asyncpg", 
        hide_password: bool = True,
        override_host=None, 
        override_port=None,
        override_db=None,
    ):
        host = override_host or self.POSTGRES_HOST
        port = override_port or self.POSTGRES_PORT
        database = override_db or self.POSTGRES_DB
        return URL.create(
            drivername=f"{self.DBMS}+{type}",
            username=self.POSTGRES_USER.get_secret_value(),
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=host,
            port=port,
            database=database,
        ).render_as_string(hide_password=hide_password)
# =======================================================
# api
class ApiEnvNames:
    API_PORT:str="API_PORT"
    class PortValues:
        DEFAULT=8000

class ApiConfig(BaseSettings):
    API_PORT:int

    @staticmethod
    def get_port()->int:
        port=int(os.environ.get(ApiEnvNames.API_PORT, ApiEnvNames.PortValues.DEFAULT))
        return port
# =======================================================
# general
class AppConfig(
    DbConfig, 
    ApiConfig,
):
    model_config = SettingsConfigDict(
        env_file=EnvPathBuilder.get_path(),
        env_file_encoding='utf-8',
        # Игнорировать, если файла нет (полезно для тестов и CI)
        extra='ignore',
    )
# =======================================================
# general
class BuildConfig:
    @staticmethod
    def get_config():
        try:
            port=ApiConfig.get_port()
            config = AppConfig(API_PORT=port,)
            return config
        except Exception as e:
            msg = (
                "Не удалось прочитать переменные окружения для config!\n"
                f"Детали:\n{e}"
            )
            raise BuildConfigError(msg)
        
config = BuildConfig.get_config()
        