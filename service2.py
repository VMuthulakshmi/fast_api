from fastapi import APIRouter, HTTPException
import logging
from logging_loki import LokiHandler
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record),
        }
        return json.dumps(log_record)

logger = logging.getLogger("service2")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
loki_handler = LokiHandler(
    url="http://localhost:3100/loki/api/v1/push",
    tags={"application": "fast_api", "service": "service2"},
    version="1",
)
loki_handler.setFormatter(JsonFormatter())
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(loki_handler)

router = APIRouter()

@router.get("/welcome")
def welcome_root():
    logger.info("Welcome endpoint called (service2)")
    return {"Welcome": "to FastAPI with Loki logging!"}

@router.get("/error")
def simulate_error():
    logger.error("Error endpoint triggered (service2)")
    raise HTTPException(status_code=400, detail="This is a simulated error")