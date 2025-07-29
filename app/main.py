from fastapi import FastAPI
from app.api.v1.endpoints import router as v1_router

app = FastAPI(title="Saber Interactive Build System")

app.include_router(v1_router, prefix="/api/v1") 