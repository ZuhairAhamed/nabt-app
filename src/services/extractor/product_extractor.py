"""
Hybrid product data extraction assistant using regex for simple cases and LLM for complex product names.
"""

import re
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser

from src.models.product import Product
from src.services.extractor.patterns import ExtractionPatterns
from src.services.extractor.cleaners import ProductNameCleaner, OriginExtractor, UnitExtractor
from src.services.classifier.product_classifier import get_classifier
from src.llm.config import get_llm, is_llm_available
from src.llm.prompts import create_extraction_prompt

logger = logging.getLogger(__name__)


class HybridProductExtractor:
    """Hybrid product extractor: regex for simple cases, LLM for complex ones."""
    
    def __init__(self, groq_api_key: Optional[str] = None):
        """
        Initialize the extractor.
        """
        # Initialize patterns and extractors
        self.patterns = ExtractionPatterns()
        self.origin_extractor = OriginExtractor(self.patterns)
        self.unit_extractor = UnitExtractor(self.patterns)
        self.name_cleaner = ProductNameCleaner(self.patterns)
        
        # Initialize LLM components if available
        self.llm_available = is_llm_available(groq_api_key)
        
        if self.llm_available:
            try:
                self.api_key = groq_api_key
                self.llm = get_llm(groq_api_key, temperature=0)
                self.output_parser = PydanticOutputParser(pydantic_object=Product)
                self._setup_llm_prompt()
                logger.info("LLM extraction enabled")
            except Exception as e:
                logger.error(f"Failed to initialize LLM: {e}")
                self.llm_available = False
        
        # Initialize classifier
        self.classifier = get_classifier(groq_api_key)
    
    def _is_complex_product_name(self, name: str) -> bool:
        """
        Determine if product name is complex enough to require LLM.
        """
        complexity_indicators = [
            len(name.split()) > 5,  # More than 5 words
            any(keyword in name.lower() for keyword in self.patterns.COMPLEXITY_KEYWORDS),
            any(char in name for char in ['-', '/', '&', '(', ')']),  # Special characters
            len(name) > 50,  # Very long names
        ]
        
        return any(complexity_indicators)
    
    def _setup_llm_prompt(self):
        """Setup LLM prompt template."""
        self.llm_prompt = create_extraction_prompt()
    
    def _extract_price(self, price_str: Any) -> float:
        """
        Extract and parse price from string.
        """
        try:
            price_clean = re.sub(r'[^\d.,]', '', str(price_str))
            price_clean = price_clean.replace(',', '.')
            return float(price_clean)
        except (ValueError, TypeError):
            logger.warning(f"Could not parse price: {price_str}")
            return 0.0
    
    def _extract_with_regex(self, raw_data: Dict[str, Any]) -> Product:
        """
        Extract product data using regex patterns.
        """
        name = raw_data.get('name', '')
        price = self._extract_price(raw_data.get('price', '0'))
        source = raw_data.get('source', '')
        
        # Extract components
        origin = self.origin_extractor.extract_origin(name)
        unit = self.unit_extractor.extract_unit(name)
        product_name = self.name_cleaner.clean_product_name(name, origin, unit)
        
        return Product(
            Original_name=name,
            ProductName=product_name,
            Unit=unit,
            Origin=origin,
            Brand=None,
            Price=price,
            Currency="SAR",
            Source=source,
            Category=None,
            Confidence=None,
            ClassificationMethod=None
        )
    
    def _call_llm(self, raw_data: Dict[str, Any]) -> Product:
        """
        Call LLM for extraction.
        """
        try:
            formatted_prompt = self.llm_prompt.format_messages(
                name=raw_data.get('name', ''),
                price=raw_data.get('price', '0'),
                source=raw_data.get('source', ''),
                format_instructions=self.output_parser.get_format_instructions()
            )
            
            response = self.llm.invoke(formatted_prompt)
            parsed_data = self.output_parser.parse(response.content)
            
            return parsed_data
            
        except Exception as e:
            raise Exception(f"LLM call failed: {str(e)}")
        
    
    def _extract_with_llm(self, raw_data: Dict[str, Any]) -> Product:
        """
        Extract product data using LLM with fallback to regex.
        """
        try:
            return self._call_llm(raw_data)
        except Exception as e:
            logger.warning(
                f"LLM extraction failed for '{raw_data.get('name', '')}', "
                f"falling back to regex: {e}"
            )
            return self._extract_with_regex(raw_data)
        
    
    def extract_product_data(self, raw_data: Dict[str, Any]) -> Product:
        """
        Extract and classify product data.
        """
        name = raw_data.get('name', '')
        
        # Choose extraction method
        if self.llm_available and self._is_complex_product_name(name):
            logger.debug(f"Using LLM extraction for: {name}")
            product_data = self._extract_with_llm(raw_data)
        else:
            logger.debug(f"Using regex extraction for: {name}")
            product_data = self._extract_with_regex(raw_data)
        
        # Classify product
        classification_result = self.classifier.classify_product(product_data.ProductName)
        product_data.Category = classification_result.category
        product_data.Confidence = classification_result.confidence
        product_data.ClassificationMethod = classification_result.method
        
        return product_data


def create_extractor(groq_api_key: Optional[str] = None) -> HybridProductExtractor:
    """
    Factory function to create a product extractor instance.
    """
    return HybridProductExtractor(groq_api_key)

