# import logging
# import sys
# import structlog


# def setup_logging() -> None:
#     logging.basicConfig(
#         format="%(message)s",
#         stream=sys.stdout,
#         level=logging.INFO,
#     )

#     structlog.configure(
#         processors=[
#             structlog.contextvars.merge_contextvars,
#             structlog.processors.TimeStamper(fmt="iso"),
#             structlog.processors.JSONRenderer(),
#         ],
#         logger_factory=structlog.stdlib.LoggerFactory(),
#         wrapper_class=structlog.stdlib.BoundLogger,
#         cache_logger_on_first_use=True,
#     )
cat > app/core/logging.py << 'EOF'
import structlog
import logging
import sys

def setup_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
EOF
