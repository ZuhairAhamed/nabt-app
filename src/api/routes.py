"""
API routes for product processing.
"""

import logging
from fastapi import HTTPException

from api.schemas import ProcessResponse, HealthResponse
from services.product_service import process_daily_products
from core.config import get_settings

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

