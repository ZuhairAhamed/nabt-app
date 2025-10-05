import json
import os
from datetime import datetime
from typing import List, Dict, Any, Tuple
import logging

from services.extractor.product_extractor import create_extractor
from database.mongo_service import upload_products
from models.product import Product

logger = logging.getLogger(__name__)


class ProductService:
    """Service class for handling product processing business logic."""
    
    def __init__(self, groq_api_key: str):
        """
        Initialize the service with API key.
        """
        self.groq_api_key = groq_api_key
        self.extractor = create_extractor(groq_api_key)
        logger.info("ProductService initialized successfully")
    
    def load_data_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Load and validate data from JSON file.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {str(e)}")
        
        if 'data' not in data:
            raise ValueError("Invalid data format. Expected 'data' key in JSON")
        
        return data['data']
    
    def process_products(
        self, 
        products: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[Product], List[Dict[str, str]]]:
        """
        Process a list of products.
        """
        results = []
        product_objects = []
        errors = []
        
        for idx, product in enumerate(products, 1):
            try:
                logger.info(f"Processing product {idx}/{len(products)}: {product.get('name', 'Unknown')}")
                
                # Extract product data
                extracted = self.extractor.extract_product_data(product)
                
                # Store Product object for MongoDB
                product_objects.append(extracted)
                
                # Convert to dict for response/file
                result = extracted.model_dump()
                results.append(result)
                
            except Exception as e:
                error_msg = f"Failed to process product {idx}: {product.get('name', 'Unknown')} - {str(e)}"
                logger.error(error_msg)
                errors.append({
                    "product_index": idx,
                    "product_name": product.get('name', 'Unknown'),
                    "error": str(e)
                })
        
        return results, product_objects, errors
    
    def save_results_to_file(self, results: List[Dict[str, Any]], output_filename: str) -> None:
        """
        Save processing results to JSON file.
        """
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {output_filename}")
    
    def upload_to_mongodb(self, product_objects: List[Product]) -> Dict[str, Any]:
        """
        Upload products to MongoDB.
        """
        save_result = upload_products(product_objects)
        logger.info(f"MongoDB save result: {save_result}")
        return save_result


def process_daily_products(groq_api_key: str, data_directory: str = "data") -> Dict[str, Any]:
    """
    Main function to process products from daily data file.
    """
    # Initialize service
    service = ProductService(groq_api_key)
    
    # Generate filename with current date
    current_date = datetime.now()
    filename = f"data-{current_date.strftime('%d-%m-%Y')}.json"
    filepath = os.path.join(data_directory, filename)
    
    logger.info(f"Processing file: {filepath}")
    
    # Load data
    products = service.load_data_file(filepath)
    logger.info(f"Found {len(products)} products to process")
    
    # Process products
    results, product_objects, errors = service.process_products(products)
    
    # Save results to file
    output_filename = f"test_data_{current_date.strftime('%d-%m-%Y')}.json"
    service.save_results_to_file(results, output_filename)
    
    # Upload to MongoDB
    service.upload_to_mongodb(product_objects)
    
    # Return summary
    processed_count = len(results)
    failed_count = len(errors)
    
    logger.info(
        f"Processing completed: {processed_count} successful, "
        f"{failed_count} failed out of {len(products)} total"
    )
    
    return {
        "status": "completed",
        "total_products": len(products),
        "processed": processed_count,
        "failed": failed_count,
        "results": results,
        "errors": errors,
        "output_file": output_filename
    }

