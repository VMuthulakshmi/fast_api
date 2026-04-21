from fastapi import FastAPI, HTTPException, Request
import logging
import json


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record),
        }
        return json.dumps(log_record)


logger = logging.getLogger("app")

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger.setLevel(logging.INFO)
logger.addHandler(handler)


app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    logger.info(f"Response: {response.status_code}")
    return response


@app.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {"Hello": "Muthu"}


@app.get("/welcome")
def welcome_root():
    logger.info("Welcome endpoint called")
    return {"Welcome": "to FastAPI with Loki logging!"}


@app.get("/error")
def simulate_error():
    logger.error("Error endpoint triggered")
    raise HTTPException(status_code=400, detail="This is a simulated error")