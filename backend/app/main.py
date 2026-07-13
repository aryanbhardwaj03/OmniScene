from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings

from app.api.router import api_router 
from app.ml.registry import model_registry

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static dir exists
os.makedirs(settings.STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    # Create database tables if they don't exist
    from app.core.database import engine, Base
    # Import models so Base.metadata knows about them
    import app.models.user  # noqa
    import app.models.analysis  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Models are loaded lazily to avoid Hugging Face Spaces health-check timeouts!

@app.on_event("shutdown")
async def shutdown_event():
    await model_registry.unload_all()

@app.get("/")
def root():
    return {"status": "running", "app": "OmniScene API", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
