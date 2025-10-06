"""
Product Comparison Service

This service provides price comparison and competitive analysis functionality
across multiple suppliers. It enables businesses to:
- Compare prices for the same products across different suppliers
- Track price trends over time
- Identify cost-saving opportunities
- Get supplier rankings and recommendations
- Calculate potential savings

The service uses MongoDB aggregation pipelines for efficient data analysis
and provides both real-time and historical comparison capabilities.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import statistics
from collections import defaultdict

from backend.database.mongo_service import get_mongo_service


class ComparisonPeriod(str, Enum):
    """Time period for price comparisons."""
    TODAY = "today"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    ALL = "all"


@dataclass
class SupplierPrice:
    """Represents a supplier's price for a specific product."""
    supplier: str
    price: float
    currency: str
    date: str
    last_updated: Optional[datetime] = None


@dataclass
class PriceStatistics:
    """Statistical analysis of prices across suppliers."""
    min_price: float
    max_price: float
    avg_price: float
    median_price: float
    variance_pct: float
    std_deviation: float
    supplier_count: int


@dataclass
class ProductComparison:
    """Complete comparison data for a single product."""
    product_name: str
    normalized_name: str
    unit: str
    category: Optional[str]
    supplier_prices: List[SupplierPrice]
    statistics: PriceStatistics
    best_price_supplier: str
    worst_price_supplier: str
    potential_savings_pct: float
    potential_savings_amount: float


@dataclass
class SavingsOpportunity:
    """Represents a potential cost-saving opportunity."""
    product_name: str
    current_supplier: str
    current_price: float
    recommended_supplier: str
    recommended_price: float
    savings_amount: float
    savings_pct: float
    category: Optional[str]


@dataclass
class PriceTrend:
    """Price trend data for a product over time."""
    product_name: str
    supplier: str
    prices: List[Tuple[str, float]]  # (date, price)
    trend_direction: str  # "increasing", "decreasing", "stable"
    change_pct: float
    volatility_score: float


def _calculate_statistics(prices: List[float]) -> PriceStatistics:
    """Calculate statistical measures for a list of prices."""
    if not prices:
        return PriceStatistics(0, 0, 0, 0, 0, 0, 0)

    min_price = min(prices)
    max_price = max(prices)
    avg_price = statistics.mean(prices)
    median_price = statistics.median(prices)

    variance_pct = ((max_price - min_price) / max_price * 100) if max_price > 0 else 0
    std_dev = statistics.stdev(prices) if len(prices) > 1 else 0

    return PriceStatistics(
        min_price=min_price,
        max_price=max_price,
        avg_price=avg_price,
        median_price=median_price,
        variance_pct=variance_pct,
        std_deviation=std_dev,
        supplier_count=len(prices)
    )


def _get_date_filter(period: ComparisonPeriod) -> Dict:
    """Get MongoDB date filter based on comparison period."""
    if period == ComparisonPeriod.ALL:
        return {}

    end_date = datetime.now()

    if period == ComparisonPeriod.TODAY:
        start_date = end_date
    elif period == ComparisonPeriod.WEEK:
        start_date = end_date - timedelta(days=7)
    elif period == ComparisonPeriod.MONTH:
        start_date = end_date - timedelta(days=30)
    elif period == ComparisonPeriod.QUARTER:
        start_date = end_date - timedelta(days=90)
    elif period == ComparisonPeriod.YEAR:
        start_date = end_date - timedelta(days=365)
    else:
        return {}

    return {
        "date": {
            "$gte": start_date.strftime("%Y-%m-%d"),
            "$lte": end_date.strftime("%Y-%m-%d")
        }
    }


class ProductComparisonService:
    """
    Service for comparing product prices across multiple suppliers.

    This service provides comprehensive price comparison capabilities including:
    - Cross-supplier price comparison
    - Historical price trend analysis
    - Savings opportunity identification
    - Supplier performance ranking
    - Price alert detection
    """

    def __init__(self):
        """Initialize the comparison service with MongoDB connection."""
        self.mongo_service = get_mongo_service()
        self.collection = self.mongo_service.collection

    def normalize_product_name(self, product_name: str, unit: str) -> str:
        """
        Normalize product name for comparison across suppliers.

        Creates a standardized identifier by combining product name and unit,
        removing variations in spacing, capitalization, and common prefixes.

        Args:
            product_name: Original product name
            unit: Product unit (e.g., "1kg", "500g")

        Returns:
            Normalized string for matching
        """
        # Convert to lowercase and remove extra spaces
        name = product_name.lower().strip()
        unit_normalized = unit.lower().strip().replace(" ", "")

        # Remove common prefixes/suffixes
        prefixes = ["fresh", "organic", "premium", "local", "imported"]
        for prefix in prefixes:
            name = name.replace(f"{prefix} ", "")

        # Create normalized key
        return f"{name}_{unit_normalized}"

    def get_product_comparison(
        self,
        product_name: str,
        period: ComparisonPeriod = ComparisonPeriod.TODAY
    ) -> Optional[ProductComparison]:
        """
        Get price comparison for a specific product across all suppliers.
        """
        date_filter = _get_date_filter(period)

        # Query all matching products (without unit filter)
        query = {
            "name": {"$regex": product_name, "$options": "i"},
            **date_filter
        }

        products = list(self.collection.find(query))

        if not products:
            return None

        # Group by supplier and get latest price
        supplier_prices: List[SupplierPrice] = []
        prices_only: List[float] = []

        supplier_latest = {}
        for product in products:
            supplier = product.get("source", "Unknown")
            date = product.get("date", "")

            # Keep only the latest entry per supplier
            if supplier not in supplier_latest or date > supplier_latest[supplier]["date"]:
                supplier_latest[supplier] = product

        # Create SupplierPrice objects
        for supplier, product in supplier_latest.items():
            price = product.get("price", 0.0)
            sp = SupplierPrice(
                supplier=supplier,
                price=price,
                currency=product.get("currency", "SAR"),
                date=product.get("date", ""),
                last_updated=datetime.now()
            )
            supplier_prices.append(sp)
            prices_only.append(price)

        if not prices_only:
            return None

        # Calculate statistics
        stats = _calculate_statistics(prices_only)

        # Find best and worst suppliers
        best_supplier = min(supplier_prices, key=lambda x: x.price)
        worst_supplier = max(supplier_prices, key=lambda x: x.price)

        # Calculate potential savings
        if stats.max_price > 0:
            savings_pct = ((stats.max_price - stats.min_price) / stats.max_price) * 100
            savings_amount = stats.max_price - stats.min_price
        else:
            savings_pct = 0.0
            savings_amount = 0.0

        # Get the most common unit from the products
        unit = products[0].get("unit", "")
        normalized_name = product_name.lower().strip()

        return ProductComparison(
            product_name=product_name,
            normalized_name=normalized_name,
            unit=unit,
            category=products[0].get("category"),
            supplier_prices=supplier_prices,
            statistics=stats,
            best_price_supplier=best_supplier.supplier,
            worst_price_supplier=worst_supplier.supplier,
            potential_savings_pct=savings_pct,
            potential_savings_amount=savings_amount
        )


# Singleton instance
_comparison_service_instance = None


def get_comparison_service() -> ProductComparisonService:
    """
    Get singleton instance of ProductComparisonService.

    Returns:
        ProductComparisonService: Singleton service instance
    """
    global _comparison_service_instance
    if _comparison_service_instance is None:
        _comparison_service_instance = ProductComparisonService()
    return _comparison_service_instance