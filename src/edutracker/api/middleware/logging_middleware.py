import time 
import logging
from fastapi import Request

logger = logging.getLogger("http")


async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
    except Exception:
        duration = (time.time() - start_time) * 1000

        logger.exception(
            "Unhandled exception",
            extra={
                "method": request.method,
                "path": request.url.path,
                "duration_ms": round(duration, 2),
            }
        )
        raise

    duration = (time.time() - start_time) * 1000

    logger.info(
        "Request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration, 2),
        },
    )

    return response