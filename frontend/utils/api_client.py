"""
API Client for Nabt Product Extractor API
"""
import requests
from typing import Optional, Dict, Any
import streamlit as st


class APIClient:
    """Client for interacting with the FastAPI backend."""

    def __init__(self, base_url: str = "http://0.0.0.0:8000"):
        self.base_url = base_url

    def health_check(self) -> Dict[str, Any]:
        """Check API health status."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def process_products(self) -> Dict[str, Any]:
        """Process products for today."""
        try:
            response = requests.post(f"{self.base_url}/api/process", timeout=300)
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_product_comparison(
        self,
        product_name: str,
        period: str = "today"
    ) -> Dict[str, Any]:
        """Get price comparison for a specific product."""
        try:
            params = {
                "product_name": product_name,
                "period": period
            }
            response = requests.get(
                f"{self.base_url}/api/comparison/product",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}


@st.cache_resource
def get_api_client(base_url: str = "http://localhost:8000") -> APIClient:
    """Get cached API client instance."""
    return APIClient(base_url)