import logging
import os
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from log import configure_logging, register_service_logger, service_context

# -----------------------------
# Setup
# -----------------------------
configure_logging()

SERVICE_1 = "user-service"
SERVICE_2 = "item-service"

register_service_logger(SERVICE_1, SERVICE_1)
register_service_logger(SERVICE_2, SERVICE_2)

user_logger = logging.getLogger(SERVICE_1)
item_logger = logging.getLogger(SERVICE_2)

app = FastAPI(title="2 Service FastAPI Demo")

# Prometheus metrics
Instrumentator().instrument(app).expose(app)


# -----------------------------
# Middleware (common logging)
# -----------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        duration = round((time.perf_counter() - start) * 1000, 2)
        user_logger.exception(
            "request_failed",
            extra=service_context(SERVICE_1, request_id=request_id, path=request.url.path)
        )
        raise

    duration = round((time.perf_counter() - start) * 1000, 2)
    response.headers["x-request-id"] = request_id

    user_logger.info(
        "request_completed",
        extra=service_context(
            SERVICE_1,
            request_id=request_id,
            path=request.url.path,
            method=request.method,
            status_code=response.status_code,
            duration_ms=duration,
        ),
    )
    return response


# -----------------------------
# Service 1 → User Service
# -----------------------------
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user_logger.info(
        "user_fetched",
        extra=service_context(SERVICE_1, user_id=user_id),
    )
    return {
        "service": SERVICE_1,
        "user_id": user_id,
        "name": f"user-{user_id}"
    }


# -----------------------------
# Service 2 → Item Service
# -----------------------------
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item_logger.info(
        "item_fetched",
        extra=service_context(SERVICE_2, item_id=item_id),
    )
    return {
        "service": SERVICE_2,
        "item_id": item_id,
        "name": f"item-{item_id}"
    }


# -----------------------------
# Health
# -----------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}


# -----------------------------
# Global Exception Handler
# -----------------------------
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    user_logger.exception(
        "unhandled_exception",
        extra=service_context(SERVICE_1, path=request.url.path),
    )
    return JSONResponse(status_code=500, content={"detail": "error"})