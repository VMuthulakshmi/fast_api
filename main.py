from fastapi import FastAPI, HTTPException, Request
import logging
import json
from logging_loki import LokiHandler

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record),
        }
        return json.dumps(log_record)

# Service 1 logger
logger_service1 = logging.getLogger("service1")
handler1 = logging.StreamHandler()
handler1.setFormatter(JsonFormatter())
loki_handler1 = LokiHandler(
    url="http://localhost:3100/loki/api/v1/push",  # Update with your Loki URL
    tags={"application": "fast_api", "service": "service1"},
    version="1",
)
loki_handler1.setFormatter(JsonFormatter())
logger_service1.setLevel(logging.INFO)
logger_service1.addHandler(handler1)
logger_service1.addHandler(loki_handler1)

# Service 2 logger
logger_service2 = logging.getLogger("service2")
handler2 = logging.StreamHandler()
handler2.setFormatter(JsonFormatter())
loki_handler2 = LokiHandler(
    url="http://localhost:3100/loki/api/v1/push",  # Update with your Loki URL
    tags={"application": "fast_api", "service": "service2"},
    version="1",
)
loki_handler2.setFormatter(JsonFormatter())
logger_service2.setLevel(logging.INFO)
logger_service2.addHandler(handler2)
logger_service2.addHandler(loki_handler2)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger_service1.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger_service1.info(f"Response: {response.status_code}")
    return response

@app.get("/")
def read_root():
    logger_service1.info("Root endpoint called (service1)")
    return {"Hello": "Muthu"}

@app.get("/welcome")
def welcome_root():
    logger_service2.info("Welcome endpoint called (service2)")
    return {"Welcome": "to FastAPI with Loki logging!"}

@app.get("/error")
def simulate_error():
    logger_service2.error("Error endpoint triggered (service2)")
    raise HTTPException(status_code=400, detail="This is a simulated error")