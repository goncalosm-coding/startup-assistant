from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Startup Assistant API",
    description="Multi-agent system for startup founders",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")