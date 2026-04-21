from fastapi import FastAPI, HTTPException, Request
import logging

# Create logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()


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