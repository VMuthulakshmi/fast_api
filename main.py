from fastapi import FastAPI, HTTPException, Request
from logger import fastapi_logger

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Muthu"}


@app.get("/welcome")
def welcome_root():
    return {"Welcome": "Sharvesh"}


@app.get("/error")
def simulate_error():
    fast_api_logger.error("Simulated error triggered")
    raise HTTPException(status_code=400, detail="This is a simulated error")

