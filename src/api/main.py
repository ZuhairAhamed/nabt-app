"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.routes import process_products, health_check
from api.schemas import ProcessResponse, HealthResponse
from core.logging import setup_logging
from core.config import get_settings

# Setup logging
settings = get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Nabt Product Extractor API",
    description="API for extracting and classifying product data using hybrid ML approach",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""
    return await health_check()


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return await health_check()


@app.post("/process", response_model=ProcessResponse)
async def process():
    """
    Process products from daily data file.
    
    This endpoint processes product data through the extraction and classification pipeline.
    """
    return await process_products()


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Nabt Product Extractor API starting up...")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Nabt Product Extractor API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

