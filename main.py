from fastapi import FastAPI
from service1 import router as service1_router
from service2 import router as service2_router

app = FastAPI()
app.include_router(service1_router)
app.include_router(service2_router)