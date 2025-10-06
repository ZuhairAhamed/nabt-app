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
    in_stock: bool = True


class PriceStatisticsSchema(BaseModel):
    """Schema for price statistics."""
    min_price: float
    max_price: float
    avg_price: float
    median_price: float
    variance_pct: float
    std_deviation: float
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


class SupplierRankingSchema(BaseModel):
    """Schema for supplier ranking."""
    supplier: str
    products_count: int
    best_price_count: int
    avg_price_position: float
    avg_discount_pct: float
    reliability_score: float
    category_strengths: Dict[str, float]


class SavingsOpportunitySchema(BaseModel):
    """Schema for savings opportunity."""
    product_name: str
    current_supplier: str
    current_price: float
    recommended_supplier: str
    recommended_price: float
    savings_amount: float
    savings_pct: float
    category: Optional[str]


class PriceTrendSchema(BaseModel):
    """Schema for price trend data."""
    product_name: str
    supplier: str
    prices: List[List]  # List of [date, price]
    trend_direction: str
    change_pct: float
    volatility_score: float


class BasketItem(BaseModel):
    """Schema for basket item."""
    product_name: str
    unit: str
    quantity: int


class BasketSavingsRequest(BaseModel):
    """Request schema for basket savings calculation."""
    basket: List[BasketItem]
    current_supplier: str
    period: str = "today"


class BasketRecommendation(BaseModel):
    """Schema for basket recommendation."""
    product: str
    unit: str
    quantity: int
    current_supplier: str
    current_unit_price: float
    current_total: float
    recommended_supplier: str
    recommended_unit_price: float
    recommended_total: float
    savings: float


class CategoryBestSupplierSchema(BaseModel):
    """Schema for category best supplier info."""
    supplier: str
    products_count: int
    best_price_count: int
    avg_discount_pct: float
    reliability_score: float


class AllComparisonsResponse(BaseModel):
    """Response schema for all comparisons."""
    total_comparisons: int
    comparisons: List[ProductComparisonSchema]


class PriceTrendsResponse(BaseModel):
    """Response schema for price trends."""
    product_name: str
    unit: str
    trends: List[PriceTrendSchema]


class CategoryBestSuppliersResponse(BaseModel):
    """Response schema for category best suppliers."""
    categories: Dict[str, CategoryBestSupplierSchema]

