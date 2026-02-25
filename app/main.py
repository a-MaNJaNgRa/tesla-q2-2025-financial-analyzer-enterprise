from app.api.v1.analyze import router as analyze_router
app.include_router(analyze_router, prefix=settings.API_V1_STR)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.middleware import request_id_middleware

settings = get_settings()

# Initialize structured logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# CORS (restricted for enterprise setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request ID middleware
app.middleware("http")(request_id_middleware)

# Prometheus metrics
Instrumentator().instrument(app).expose(app)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    return {"status": "ready"}