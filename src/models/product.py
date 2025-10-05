"""
Product data models.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    """Product model with all extracted and classified information."""
    
    Original_name: str = Field(..., description="Original product name from source")
    ProductName: str = Field(..., description="Cleaned and extracted product name")
    Unit: str = Field(..., description="Unit of measurement (e.g., '1 kg', '500g', '1 piece')")
    Origin: Optional[str] = Field(None, description="Country or region of origin")
    Brand: Optional[str] = Field(None, description="Brand name if applicable")
    Price: float = Field(..., description="Product price")
    Currency: str = Field(..., description="Currency code (e.g., 'SAR', 'USD')")
    Source: str = Field(..., description="Data source/provider")
    Category: Optional[str] = Field(None, description="Product category")
    Confidence: Optional[float] = Field(None, description="Classification confidence score (0-1)")
    ClassificationMethod: Optional[str] = Field(None, description="Method used for classification")


