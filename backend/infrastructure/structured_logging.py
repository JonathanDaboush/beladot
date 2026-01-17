import re
# Helper to inject request_id into logs
def redact_pii(data):
    if isinstance(data, dict):
        return {k: ("[REDACTED]" if re.search(r"email|password|secret", k, re.I) else v) for k, v in data.items()}
    return data
import structlog
import logging
import sys
from fastapi import Request
import datetime

# Configure structlog for JSON output
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Helper to inject request_id into logs
async def log_request_start(request: Request):
    logger.info(
        "request.start",
        method=request.method,
        path=request.url.path,
        request_id=getattr(request.state, "request_id", None),
        correlation_id=getattr(request.state, "correlation_id", None),
        client=request.client.host if request.client else None,
        severity="INFO"
    )

async def log_request_end(request: Request, status_code: int, latency: float):
    logger.info(
        "request.end",
        method=request.method,
        path=request.url.path,
        status_code=status_code,
        latency=latency,
        request_id=getattr(request.state, "request_id", None),
        correlation_id=getattr(request.state, "correlation_id", None),
        severity="INFO"
    )
def log_event(event, data):
    logger.info(event, **redact_pii(data), severity="INFO")

def log_error_event(event, data):
    logger.error(event, **redact_pii(data), severity="ERROR")

def audit_event(event_type, actor, entity, details):
    # Immutable audit record (append-only)
    with open("audit.log", "a") as f:
        f.write(f"{datetime.datetime.now().isoformat()}|{event_type}|{actor}|{entity}|{details}\n")
# Usage: import logger, log_request_start, log_request_end
