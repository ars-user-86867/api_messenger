from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
# from authx.exceptions import JWTDecodeError, MissingTokenError
# from src.api.routes.service import exc

# def add_jwt_exceptions(app: FastAPI):
#     @app.exception_handler(exc.RateLimitError)
#     async def rate_limit_handler(request: Request, exc: exc.RateLimitError):
#         return JSONResponse(
#             status_code=429,
#             content={"message": "Пожалуйста, подождите, мы делаем слишком много запросов."},
#         )
    # @app.exception_handler(JWTDecodeError)
    # async def jwt_decode_error_handler(request: Request, exc: JWTDecodeError):
    #     """
    #     Обработчик для ошибок декодирования JWT токена.
    #     Возвращает статус 401 Unauthorized с деталями ошибки.
    #     """
    #     return JSONResponse(
    #         status_code=401,
    #         content={"detail": "Недействительный или повреждённый JWT токен."},
    #     )
    # @app.exception_handler(MissingTokenError)
    # async def missing_token_error_handler(request: Request, exc: MissingTokenError):
    #     """
    #     Обработчик для ошибок декодирования JWT токена.
    #     Возвращает статус 401 Unauthorized с деталями ошибки.
    #     """
    #     return JSONResponse(
    #         status_code=401,
    #         content={"detail": "Отсутствует JWT токен в запросе."},
    #     )

class FastApiError(Exception):
    ...

class SetupMiddlewareUrlsError(FastApiError):
    ...

class AddMiddlewareError(FastApiError):
    ...

class SetupFastApiRoutes(FastApiError):
    ...