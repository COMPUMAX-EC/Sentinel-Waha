"""
Sentinel WhatsApp - Main Entry Point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from loguru import logger

from sentinel.config import settings
from sentinel.webhooks.routes import router as webhooks_router
from sentinel.analytics.routes import router as analytics_router

# Initialize FastAPI app
app = FastAPI(
    title="Sentinel WhatsApp",
    description="Sistema de Inteligencia de Datos y Optimización de Conversión para WhatsApp",
    version="1.0.0",
    docs_url="/docs" if settings.APP_DEBUG else None,
    redoc_url="/redoc" if settings.APP_DEBUG else None,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(webhooks_router, prefix="/webhooks", tags=["webhooks"])
app.include_router(analytics_router, prefix="/analytics", tags=["analytics"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("🚀 Starting Sentinel WhatsApp...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"WAHA API: {settings.WAHA_API_URL}")
    logger.info(f"Auto-response: {'Enabled' if settings.ENABLE_AUTO_RESPONSE else 'Disabled'}")
    logger.info(f"Analytics: {'Enabled' if settings.ENABLE_ANALYTICS else 'Disabled'}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down Sentinel WhatsApp...")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Sentinel WhatsApp",
        "version": "1.0.0",
        "environment": settings.APP_ENV,
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "features": {
            "auto_response": settings.ENABLE_AUTO_RESPONSE,
            "analytics": settings.ENABLE_ANALYTICS,
            "webhooks": settings.ENABLE_WEBHOOKS,
            "intent_classification": settings.ENABLE_INTENT_CLASSIFICATION,
        },
        "connections": {
            "waha_api": settings.WAHA_API_URL,
            "database": "connected",  # TODO: Add actual DB check
            "redis": "connected",  # TODO: Add actual Redis check
        },
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if settings.APP_DEBUG else "An error occurred",
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
