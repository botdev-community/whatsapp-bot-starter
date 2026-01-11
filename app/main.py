"""
WhatsApp Bot Starter - Main Application
Built by BotDev Community
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.config import settings
from app.routers import webhook
from app.utils.logger import setup_logging
from app.services.database import Database

# Setup logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="WhatsApp Bot Starter",
    description="Production-ready WhatsApp bot using FastAPI and WhatsApp Cloud API",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting WhatsApp Bot application...")
    
    # Initialize database connection
    try:
        db = Database()
        await db.connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
    
    logger.info(f"Application started in {settings.ENVIRONMENT} mode")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down WhatsApp Bot application...")
    
    # Close database connection
    try:
        db = Database()
        await db.close()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "WhatsApp Bot Starter API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "disabled"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db = Database()
        db_status = await db.ping()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "database": "connected" if db_status else "disconnected",
                "environment": settings.ENVIRONMENT
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
