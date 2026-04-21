import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any

import logging_loki

LOKI_URL = "http://loki-gateway.loki.svc.cluster.local/loki/api/v1/push"


def service_context(service_name: str, **extra: Any):
    return {
        "service": service_name,
        **extra
    }


class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": getattr(record, "service", "unknown"),
            **record.__dict__,
        })


def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel("INFO")


def register_service_logger(name: str, service: str):
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel("INFO")
    logger.propagate = False

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(JsonFormatter())
    logger.addHandler(console)

    loki_handler = logging_loki.LokiHandler(
        url=LOKI_URL,
        tags={"service": service},
        version="1",
    )
    logger.addHandler(loki_handler)