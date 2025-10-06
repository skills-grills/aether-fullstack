from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from .config import settings
from .api.endpoints import reports

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Report Generation Service",
    description="A service that generates detailed reports using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(
    reports.router,
    prefix="/api/v1",
    tags=["reports"]
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup"""
    logger.info("Starting up AI Report Generation Service...")
    # Any initialization code can go here

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on application shutdown"""
    logger.info("Shutting down AI Report Generation Service...")
    # Any cleanup code can go here

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

# Run with uvicorn programmatically
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )
