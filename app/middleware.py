from time import time
from starlette.middleware.base import BaseHTTPMiddleware
from .logger import get_logger

logger = get_logger("http")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time()
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as exc:
            duration = time() - start
            logger.error(
                "request failed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(exc),
                    "latency_ms": round(duration * 1000, 2),
                },
            )
            raise

        duration = time() - start
        logger.info(
            "request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "latency_ms": round(duration * 1000, 2),
            },
        )

        return response


logging_middleware = LoggingMiddleware
