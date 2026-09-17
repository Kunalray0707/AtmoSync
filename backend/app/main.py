"""AtmoSync Backend - FastAPI Application Entry Point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.auth import router as auth_router
from app.api.commodities import router as commodities_router
from app.api.sensors import router as sensors_router
from app.api.alerts import router as alerts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    # Startup
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    await init_db()
    print("Database tables initialized")
    yield
    # Shutdown
    await close_db()
    print("Database connections closed")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Micro-Climate Arbitrage Analytics Platform API",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(auth_router, prefix="/api/v1")
app.include_router(commodities_router, prefix="/api/v1")
app.include_router(sensors_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }
