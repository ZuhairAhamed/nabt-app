"""
MongoDB service for product data storage.
"""

import logging
from typing import List, Dict, Any
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime

from core.config import get_settings
from models.product import Product

logger = logging.getLogger(__name__)


class MongoDBService:
    """MongoDB service for managing product data."""
    
    def __init__(self):
        """Initialize MongoDB connection."""
        settings = get_settings()
        self.client = MongoClient(settings.mongodb_uri)
        self.db = self.client[settings.mongodb_database]
        self.collection = self.db[settings.mongodb_collection]
        
        # Ensure indexes for faster queries
        self._create_indexes()
        logger.info(f"MongoDB service initialized: {settings.mongodb_database}.{settings.mongodb_collection}")
    
    def _create_indexes(self):
        """Create indexes for optimized queries."""
        try:
            self.collection.create_index([("date", 1), ("name", 1)])
            self.collection.create_index([("date", 1), ("source", 1)])
            logger.info("MongoDB indexes created successfully")
        except PyMongoError as e:
            logger.warning(f"Failed to create indexes: {e}")
    
    def insert_products(self, products: List[Product]) -> Dict[str, Any]:
        """
        Insert products into MongoDB.
        
        Args:
            products: List of Product objects to insert
            
        Returns:
            Dict containing status and count
            
        Raises:
            PyMongoError: If database operation fails
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            docs = []
            for p in products:
                doc = {
                    "date": today,
                    "name": p.ProductName,
                    "origin": p.Origin,
                    "brand": p.Brand,
                    "unit": p.Unit,
                    "price": p.Price,
                    "currency": p.Currency,
                    "source": p.Source,
                    "category": p.Category,
                    "confidence": p.Confidence,
                    "classification_method": p.ClassificationMethod,
                    "original_name": p.Original_name
                }
                docs.append(doc)
            
            if docs:
                result = self.collection.insert_many(docs)
                logger.info(f"Inserted {len(result.inserted_ids)} products into MongoDB")
                return {
                    "status": "success",
                    "inserted_count": len(result.inserted_ids)
                }
            else:
                logger.warning("No products to insert")
                return {
                    "status": "success",
                    "inserted_count": 0
                }
        
        except PyMongoError as e:
            logger.error(f"Failed to insert products: {e}")
            raise
    
    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Global service instance
_mongo_service = None


def get_mongo_service() -> MongoDBService:
    """
    Get or create MongoDB service instance.
    
    Returns:
        MongoDBService: MongoDB service instance
    """
    global _mongo_service
    if _mongo_service is None:
        _mongo_service = MongoDBService()
    return _mongo_service


def upload_products(products: List[Product]) -> Dict[str, Any]:
    """
    Upload products to MongoDB.
    
    Args:
        products: List of Product objects to upload
        
    Returns:
        Dict containing status and count
    """
    service = get_mongo_service()
    return service.insert_products(products)

