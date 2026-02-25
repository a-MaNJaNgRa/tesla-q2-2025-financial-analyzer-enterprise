import time
import uuid
from fastapi import Request
import structlog


logger = structlog.get_logger()


async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())

    # Bind request_id into structured logs
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=round(process_time, 2),
    )

    response.headers["X-Request-ID"] = request_id

    return response