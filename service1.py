from fastapi import APIRouter
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

logger = logging.getLogger("service1")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
loki_handler = LokiHandler(
    url="http://localhost:3100/loki/api/v1/push",
    tags={"application": "fast_api", "service": "service1"},
    version="1",
)
loki_handler.setFormatter(JsonFormatter())
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(loki_handler)

router = APIRouter()

@router.get("/")
def read_root():
    logger.info("Root endpoint called (service1)")
    return {"Hello": "Muthu"}