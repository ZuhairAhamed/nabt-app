"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.api.routes import (
    process_products,
    health_check,
    get_product_comparison_route,
)
from src.api.schemas import (
    ProcessResponse,
    HealthResponse,
    ProductComparisonSchema,
)
from src.core.logging import setup_logging
from src.core.config import get_settings

# Setup logging
settings = get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Product Extractor API",
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


@app.post("/api/process", response_model=ProcessResponse)
async def process():
    """Process products from daily data file."""
    return await process_products()


@app.get("/api/comparison/product", response_model=ProductComparisonSchema, tags=["Comparison"])
async def get_product_comparison(product_name: str, period: str = "today"):
    """Get price comparison for a specific product across all suppliers. """
    return await get_product_comparison_route(product_name, period)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Product Extractor API starting up...")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Product Extractor API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

