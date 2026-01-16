import sys

# Формат логов (можно сделать похожим на Uvicorn или JSON для продакшена)
LOG_FORMAT = (
    "%(levelname)s:     "
    "%(name)s - "
    "%(asctime)s - "
    "%(message)s"
)

# Словарь конфигурации
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # ВАЖНО: Не отключать логгеры Uvicorn/SQLAlchemy
    "formatters": {
        "standard": {
            "format": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        # Настройка корневого логгера (захватит все библиотеки и твой код)
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        # Настройка тестов приложения (чтобы видеть DEBUG именно твоего кода)
        "tests": { 
            "handlers": ["console"],
            "level": "DEBUG", 
            "propagate": False, # Чтобы не дублировалось в root
        },
        # Настройка твоего приложения (чтобы видеть DEBUG именно твоего кода)
        "src": { 
            "handlers": ["console"],
            "level": "DEBUG", 
            "propagate": False, # Чтобы не дублировалось в root
        },
        # Можно принудительно настроить Uvicorn, чтобы формат совпадал
        # "uvicorn": {
        #     "handlers": ["console"],
        #     "level": "INFO",
        #     "propagate": False,
        # },
        # "uvicorn.error": {
        #     "level": "INFO",
        # },
        # "uvicorn.access": {
        #     "handlers": ["console"],
        #     "level": "INFO",
        #     "propagate": False,
        # },
    },
}