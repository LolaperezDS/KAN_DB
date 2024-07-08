from fastapi import FastAPI
from api_v1 import router as api_v1_router

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
app.include_router(api_v1_router, prefix="/api/v1")
Instrumentator().instrument(app).expose(app)
