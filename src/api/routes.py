"""
API routes for product processing and comparison.
"""

import logging
from typing import Optional
from fastapi import HTTPException, Query

from src.api.schemas import (
    ProcessResponse,
    HealthResponse,
    ProductComparisonSchema,
    AllComparisonsResponse,
    PriceTrendsResponse,
    BasketSavingsRequest,
    CategoryBestSuppliersResponse,
    SupplierPriceSchema,
    PriceStatisticsSchema,
    SupplierRankingSchema,
    SavingsOpportunitySchema,
    PriceTrendSchema,
    BasketRecommendation,
    CategoryBestSupplierSchema
)
from src.services.product_service import process_daily_products
from src.services.product_comparison_service import get_comparison_service, ComparisonPeriod
from src.core.config import get_settings

logger = logging.getLogger(__name__)


async def process_products() -> ProcessResponse:
    """
    Process products from daily data file.
    """
    try:
        # Get API key from settings
        settings = get_settings()
        groq_api_key = settings.groq_api_key
        
        if not groq_api_key:
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY is not configured. Please set it in the .env file."
            )
        
        # Call business logic
        result = process_daily_products(groq_api_key, settings.data_directory)
        
        # Return response
        return ProcessResponse(
            status=result["status"],
            total_products=result["total_products"],
            processed=result["processed"],
            failed=result["failed"],
            results=result["results"],
            errors=result["errors"],
            output_file=result.get("output_file")
        )
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    """
    return HealthResponse(status="healthy", version="1.0.0")


# ==================== Comparison Routes ====================

def _convert_comparison_to_schema(comparison) -> ProductComparisonSchema:
    """Convert ProductComparison dataclass to Pydantic schema."""
    return ProductComparisonSchema(
        product_name=comparison.product_name,
        normalized_name=comparison.normalized_name,
        unit=comparison.unit,
        category=comparison.category,
        supplier_prices=[
            SupplierPriceSchema(
                supplier=sp.supplier,
                price=sp.price,
                currency=sp.currency,
                date=sp.date,
                in_stock=sp.in_stock
            )
            for sp in comparison.supplier_prices
        ],
        statistics=PriceStatisticsSchema(
            min_price=comparison.statistics.min_price,
            max_price=comparison.statistics.max_price,
            avg_price=comparison.statistics.avg_price,
            median_price=comparison.statistics.median_price,
            variance_pct=comparison.statistics.variance_pct,
            std_deviation=comparison.statistics.std_deviation,
            supplier_count=comparison.statistics.supplier_count
        ),
        best_price_supplier=comparison.best_price_supplier,
        worst_price_supplier=comparison.worst_price_supplier,
        potential_savings_pct=comparison.potential_savings_pct,
        potential_savings_amount=comparison.potential_savings_amount
    )


async def get_product_comparison_route(
    product_name: str = Query(..., description="Product name to compare"),
    unit: str = Query(..., description="Product unit (e.g., '1kg', '500g')"),
    period: str = Query("today", description="Time period: today, week, month, quarter, year, all")
) -> ProductComparisonSchema:
    """
    Get price comparison for a specific product across all suppliers.

    Returns detailed comparison including all supplier prices, statistics,
    and potential savings.
    """
    try:
        comparison_service = get_comparison_service()
        period_enum = ComparisonPeriod(period.lower())

        comparison = comparison_service.get_product_comparison(
            product_name=product_name,
            unit=unit,
            period=period_enum
        )

        if not comparison:
            raise HTTPException(
                status_code=404,
                detail=f"Product '{product_name}' with unit '{unit}' not found"
            )

        return _convert_comparison_to_schema(comparison)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid period value: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting product comparison: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


async def get_all_comparisons_route(
    category: Optional[str] = Query(None, description="Filter by category"),
    min_suppliers: int = Query(2, description="Minimum number of suppliers required"),
    period: str = Query("today", description="Time period: today, week, month, quarter, year, all")
) -> AllComparisonsResponse:
    """
    Get price comparisons for all products with multiple suppliers.

    Returns a list of all products that have prices from multiple suppliers,
    sorted by potential savings amount.
    """
    try:
        comparison_service = get_comparison_service()
        period_enum = ComparisonPeriod(period.lower())

        comparisons = comparison_service.get_all_comparisons(
            category=category,
            min_suppliers=min_suppliers,
            period=period_enum
        )

        comparison_schemas = [_convert_comparison_to_schema(c) for c in comparisons]

        return AllComparisonsResponse(
            total_comparisons=len(comparison_schemas),
            comparisons=comparison_schemas
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting all comparisons: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


async def get_price_trends_route(
    product_name: str = Query(..., description="Product name"),
    unit: str = Query(..., description="Product unit"),
    supplier: Optional[str] = Query(None, description="Specific supplier (optional)"),
    days: int = Query(30, description="Number of days to analyze")
) -> PriceTrendsResponse:
    """
    Get historical price trends for a product.

    Returns price history, trend direction, and volatility analysis
    for the specified product across suppliers.
    """
    try:
        comparison_service = get_comparison_service()

        trends = comparison_service.get_price_trends(
            product_name=product_name,
            unit=unit,
            supplier=supplier,
            days=days
        )

        if not trends:
            raise HTTPException(
                status_code=404,
                detail=f"No price history found for '{product_name}' ({unit})"
            )

        trend_schemas = [
            PriceTrendSchema(
                product_name=t.product_name,
                supplier=t.supplier,
                prices=t.prices,
                trend_direction=t.trend_direction,
                change_pct=t.change_pct,
                volatility_score=t.volatility_score
            )
            for t in trends
        ]

        return PriceTrendsResponse(
            product_name=product_name,
            unit=unit,
            trends=trend_schemas
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting price trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


async def get_category_best_suppliers_route(
    period: str = Query("month", description="Time period: today, week, month, quarter, year, all")
) -> CategoryBestSuppliersResponse:
    """
    Get the best supplier for each product category.

    Returns the top-performing supplier for each category based on
    pricing, product availability, and reliability.
    """
    try:
        comparison_service = get_comparison_service()
        period_enum = ComparisonPeriod(period.lower())

        category_leaders = comparison_service.get_category_best_suppliers(period=period_enum)

        category_schemas = {
            category: CategoryBestSupplierSchema(
                supplier=info["supplier"],
                products_count=info["products_count"],
                best_price_count=info["best_price_count"],
                avg_discount_pct=info["avg_discount_pct"],
                reliability_score=info["reliability_score"]
            )
            for category, info in category_leaders.items()
        }

        return CategoryBestSuppliersResponse(categories=category_schemas)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting category best suppliers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

