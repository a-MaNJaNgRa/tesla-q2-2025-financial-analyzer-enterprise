mkdir -p app/core
cat > app/core/middleware.py << 'EOF'
import time
import uuid
from fastapi import Request
import structlog
from slowapi import Limiter
from slowapi.util import get_remote_address

logger = structlog.get_logger()
limiter = Limiter(key_func=get_remote_address)

async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info("request_completed", 
                status_code=response.status_code, 
                duration_ms=round(duration*1000, 2),
                path=request.url.path)
    return response
EOF
