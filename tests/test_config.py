from src.utils.config.build import BuildConfig, AppConfig
from src.utils.config.build import (
    DbEnvNames, ApiEnvNames,
)

POSTGRES_HOST = "testhost"
POSTGRES_PORT = 1234
POSTGRES_USER = "test_user"
POSTGRES_PASSWORD = "test_password"
POSTGRES_DB = "test_db"
DBMS = "postgresql"
POSTGRES_SCHEMA = "test_schema"

API_PORT = 1235

class TestAppConfig:
    # @pytest.fixture(autouse=True)
    def get_config(self):
        self.config:AppConfig = BuildConfig.get_config()

    def _setup_db_env(self, monkeypatch):
        monkeypatch.setenv(DbEnvNames.POSTGRES_HOST, POSTGRES_HOST)
        monkeypatch.setenv(DbEnvNames.POSTGRES_PORT, POSTGRES_PORT)
        monkeypatch.setenv(DbEnvNames.POSTGRES_USER, POSTGRES_USER)
        monkeypatch.setenv(DbEnvNames.POSTGRES_PASSWORD, POSTGRES_PASSWORD)
        monkeypatch.setenv(DbEnvNames.POSTGRES_DB, POSTGRES_DB)
        monkeypatch.setenv(DbEnvNames.POSTGRES_SCHEMA, POSTGRES_SCHEMA)
        monkeypatch.setenv(DbEnvNames.DBMS, DBMS)

    def _assert_db_env(self):
        assert self.config.POSTGRES_HOST == POSTGRES_HOST
        assert self.config.POSTGRES_PORT == POSTGRES_PORT
        assert self.config.POSTGRES_USER.get_secret_value() == POSTGRES_USER
        assert self.config.POSTGRES_PASSWORD.get_secret_value() == POSTGRES_PASSWORD
        assert self.config.POSTGRES_DB == POSTGRES_DB
        assert self.config.POSTGRES_SCHEMA == POSTGRES_SCHEMA
        assert self.config.DBMS == DBMS

    def test_general_config(self, monkeypatch):
        self._setup_db_env(monkeypatch)
        self.get_config()

        url = self.config.DATABASE_URL(hide_password=False) 
        print(url)
        self._assert_db_env()

    def test_api_config(self, monkeypatch):
        monkeypatch.setenv(ApiEnvNames.API_PORT, API_PORT)
        self.get_config()

        assert self.config.API_PORT == API_PORT
