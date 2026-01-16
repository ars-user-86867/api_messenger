import logging.config
from src.utils.logs.exc import LoggerSetupError

class BaseLogger:
    @staticmethod
    def setup_logger():
        try:
            from src.utils.logs.config import LOGGING_CONFIG
            logging.config.dictConfig(LOGGING_CONFIG)
            logging.info("setup logger success")
        except Exception as e:
            msg = (
                "Не удалось настроить логгер!\n"
                f"Детали:\n{e}"
            )
            raise LoggerSetupError(msg)    
    