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
    get_all_comparisons_route,
    get_price_trends_route,
    get_category_best_suppliers_route
)
from src.api.schemas import (
    ProcessResponse,
    HealthResponse,
    ProductComparisonSchema,
    AllComparisonsResponse,
    PriceTrendsResponse,
    BasketSavingsRequest,
    CategoryBestSuppliersResponse
)
from src.core.logging import setup_logging
from src.core.config import get_settings

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


@app.post("/api/process", response_model=ProcessResponse)
async def process():
    return await process_products()


# ==================== Comparison Endpoints ====================

@app.get("/api/comparison/product", response_model=ProductComparisonSchema, tags=["Comparison"])
async def get_product_comparison(
    product_name: str,
    unit: str,
    period: str = "today"
):
    """
    Get price comparison for a specific product across all suppliers.
    """
    return await get_product_comparison_route(product_name, unit, period)


@app.get("/api/comparison/all", response_model=AllComparisonsResponse, tags=["Comparison"])
async def get_all_comparisons(
    category: str = None,
    min_suppliers: int = 2,
    period: str = "today"
):
    """
    Get price comparisons for all products with multiple suppliers.
    """
    return await get_all_comparisons_route(category, min_suppliers, period)


@app.get("/api/comparison/trends", response_model=PriceTrendsResponse, tags=["Comparison"])
async def get_price_trends(
    product_name: str,
    unit: str,
    supplier: str = None,
    days: int = 30
):
    """
    Get historical price trends for a product.
    """
    return await get_price_trends_route(product_name, unit, supplier, days)

@app.get("/api/comparison/categories/best", response_model=CategoryBestSuppliersResponse, tags=["Comparison"])
async def get_category_best_suppliers(period: str = "month"):
    """
    Get the best supplier for each product category.
    """
    return await get_category_best_suppliers_route(period)


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
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

