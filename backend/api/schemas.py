"""
API request and response schemas.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ProcessResponse(BaseModel):
    """Response model for processed products."""

    status: str = Field(..., description="Processing status")
    total_products: int = Field(..., description="Total number of products in input")
    processed: int = Field(..., description="Number of successfully processed products")
    failed: int = Field(..., description="Number of failed products")
    results: List[Dict[str, Any]] = Field(..., description="List of processed product data")
    errors: List[Dict[str, str]] = Field(default_factory=list, description="List of errors encountered")
    output_file: Optional[str] = Field(None, description="Output file path if saved")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }


# ==================== Comparison API Schemas ====================

class SupplierPriceSchema(BaseModel):
    """Schema for supplier price information."""
    supplier: str
    price: float
    currency: str
    date: str


class PriceStatisticsSchema(BaseModel):
    """Schema for price statistics."""
    min_price: float
    max_price: float
    avg_price: float
    supplier_count: int


class ProductComparisonSchema(BaseModel):
    """Schema for product comparison response."""
    product_name: str
    normalized_name: str
    unit: str
    category: Optional[str]
    supplier_prices: List[SupplierPriceSchema]
    statistics: PriceStatisticsSchema
    best_price_supplier: str
    worst_price_supplier: str
    potential_savings_pct: float
    potential_savings_amount: float

