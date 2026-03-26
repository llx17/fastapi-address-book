import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        logger.info("Incoming request: %s %s", request.method, request.url.path)

        response = await call_next(request)

        duration = time.perf_counter() - start_time

        logger.info(
            "Completed request: %s %s | Status: %s | Duration: %.4fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response