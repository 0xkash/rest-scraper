import time

from typing import List

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

from starlette.middleware.base import BaseHTTPMiddleware

from .config import Config
from .logger import Logger

logger = Logger(__name__)

class ExceptionHandler:
    @staticmethod
    def handle(request: Request, exception: Exception|RequestValidationError) -> JSONResponse:
        if isinstance(exception, RequestValidationError):
            error = exception.errors()[0]
            message = 'Validation error: {} {}'.format('.'.join(error['loc']), error['msg'])
            logger.error(message)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": message
                }
            )

        message = 'An error occured during {} handling. Error: {}'.format(
            request.state.func_name,
            exception
        )
        logger.error(message)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": message
            }
        )

class RequestHandler(BaseHTTPMiddleware):
    def __get_request_handler(self, request: Request) -> str|None:
        routes: List[APIRoute] = request.app.routes
        for route in routes:
            if route.path == request.url.path:
                return "`{}()`".format(route.endpoint.__name__)

    async def dispatch(self, request: Request, call_next):
        if Config.get("ENVIRONMENT") == "production":
            return await call_next(request)

        # Only log requests in development environment
        logger.info('Request: {} {}'.format(request.method, request.url.path))
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)

        logger.info('Response: {} from {} - proccessed in (ms): {}'.format(
            response.status_code,
            self.__get_request_handler(request),
            formatted_process_time
        ))
        return response