from enum import Enum
import logging
import asyncio
from functools import wraps
import inspect
import time
import traceback
from typing import Callable, TypeVar, ParamSpec

from src.utils.deco.exc import RepeatDecoError

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")

class Formatting:
    @staticmethod
    def print_padded_line(text: str = "", width: int = 100, pad_char: str = "="):
        """
        Печатает строку, центрированную и обрамленную символами.

        :param text: Текст для отображения в центре. Если пустой, печатается сплошная линия.
        :param width: Общая ширина строки.
        :param pad_char: Символ для обрамления.
        """
        if not text:
            # Если текст пустой, просто печатаем сплошную линию
            line = pad_char * width
            return line
        else:
            # Форматируем текст с пробелами по бокам и центрируем его,
            # заполняя оставшееся пространство символом pad_char
            formatted_text = f" {text} ".center(width, pad_char)
            # print(formatted_text)
            return formatted_text

    @staticmethod
    def formatted_dict(header:str, iterable:dict | tuple | list):
        msg:str = f'\n{Formatting.print_padded_line(header)}\n'
        if isinstance(iterable, dict):
            max_key_len = max(len(k) for k in iterable.keys())
            for key, value in iterable.items():
                if isinstance(value, Enum):
                    value = value.value
                msg+=(f'\t{key:<{max_key_len}} : {value}\n')
        elif isinstance(iterable, tuple):
            max_key_len = len(str(len(iterable) - 1)) if iterable else 1
            for i, value in enumerate(iterable):
                if isinstance(value, Enum):
                    value = value.value
                msg+=(f'\t{i:<{max_key_len}} : {value}\n')  
        elif isinstance(iterable, list):
            max_key_len = len(str(len(iterable) - 1)) if iterable else 1
            for i, value in enumerate(iterable):
                if isinstance(value, Enum):
                    value = value.value
                msg+=(f'\t{i:<{max_key_len}} : {value}\n')              
        msg+=Formatting.print_padded_line()
        return msg

class Deco:
    @staticmethod
    def _log_error_details(
        func: Callable, 
        e: Exception, 
        *args: P.args, 
        **kwargs: P.kwargs
    ):
        """Вспомогательный метод для логирования деталей ошибки."""
        _trace = traceback.format_exc()
        if args:
            _args = Formatting.formatted_dict("Позиционные аргументы (args):", *args)
        else:
            _args = "Позиционные аргументы отсутствуют."
        if kwargs:
            _kwargs = Formatting.formatted_dict("Именованные аргументы (kwargs):", kwargs)
        else:
            _kwargs = "Именованные аргументы отсутствуют."
        msg = (
            f'Произошла ошибка в функции "{func.__name__}": {e}\n{_trace}'
            f'{_args}'
            f'{_kwargs}'
        )
        logger.error(msg)

    @staticmethod
    def is_error(func: Callable[P, R]) -> Callable[P, R]:
        """Декоратор для логирования ошибок в синхронных и асинхронных функциях."""
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    Deco._log_error_details(func, e, *args, **kwargs)
                    raise
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    Deco._log_error_details(func, e, *args, **kwargs)
                    raise
            return sync_wrapper

    @staticmethod
    def _get_timer_log(func_name: str, start: float):
        """Вспомогательный метод для логирования времени"""
        stop = time.perf_counter()
        logger.debug(f'runtime func "{func_name}": {stop - start:.3f} сек')

    @staticmethod
    def _sleep(seconds: float, is_async: bool):
        """Универсальный sleep (вызывает либо time, либо возвращает корутину)"""
        if is_async:
            return asyncio.sleep(seconds)
        time.sleep(seconds)
        return None

    @classmethod
    def retry(cls, tries: int = 3, delay: float = 0.0):
        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            is_async = inspect.iscoroutinefunction(func)

            if is_async:
                @wraps(func)
                async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                    last_error = None
                    for i in range(1, tries + 1):
                        try:
                            logger.debug(f'run async func "{func.__name__}" (attempt {i})')
                            start = time.perf_counter()
                            # В асинхронном коде МЫ ОБЯЗАНЫ явно писать await
                            result = await func(*args, **kwargs) 
                            cls._get_timer_log(func.__name__, start)
                            return result
                        except Exception as e:
                            last_error = e
                            if i < tries:
                                await cls._sleep(delay, is_async=True)
                    raise RepeatDecoError(
                        f"Max retries ({tries}) exhausted for {func.__name__}. Last error: {last_error}"
                    ) from last_error
            else:
                @wraps(func)
                def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                    last_error = None
                    for i in range(1, tries + 1):
                        try:
                            logger.debug(f'run sync func "{func.__name__}" (attempt {i})')
                            start = time.perf_counter()
                            result = func(*args, **kwargs)
                            cls._get_timer_log(func.__name__, start)
                            return result
                        except Exception as e:
                            last_error = e
                            if i < tries:
                                cls._sleep(delay, is_async=False)
                    raise RepeatDecoError(
                        f"Max retries ({tries}) exhausted for {func.__name__}. Last error: {last_error}"
                    ) from last_error
            
            return wrapper # type: ignore
        return decorator

deco = Deco()