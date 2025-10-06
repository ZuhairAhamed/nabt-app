"""
Product name cleaning utilities.
"""

import re
import logging
from typing import Optional

from backend.services.extractor.patterns import ExtractionPatterns

logger = logging.getLogger(__name__)


class ProductNameCleaner:
    # Cleans product names by removing descriptive words, origin, and units

    def __init__(self, patterns: ExtractionPatterns):
        # Initialize cleaner with extraction patterns
        self.patterns = patterns
        self.descriptive_regex = re.compile(
            patterns.get_descriptive_pattern(), 
            re.IGNORECASE
        )
    
    def clean_product_name(self, name: str, origin: Optional[str] = None, unit: Optional[str] = None) -> str:
        # Clean product name by removing origin, units, and descriptive words
        clean_name = name
        
        # Remove origin
        if origin:
            clean_name = re.sub(
                rf'\b{re.escape(origin)}\b', 
                '', 
                clean_name, 
                flags=re.IGNORECASE
            )
        
        # Remove unit information
        if unit and unit != "1 piece":
            clean_name = re.sub(
                re.escape(unit), 
                '', 
                clean_name, 
                flags=re.IGNORECASE
            )
        
        # Remove descriptive words
        clean_name = self.descriptive_regex.sub('', clean_name)
        
        # Clean up extra spaces
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()
        
        # Fallback: extract meaningful words if name too short
        if len(clean_name) < 2:
            clean_name = self._extract_core_product_word(name)
        
        return clean_name
    
    def _extract_core_product_word(self, name: str) -> str:
        # Extract the core product word when cleaning removes too much
        words = name.split()
        exclude_words = (
            self.patterns.UNIT_KEYWORDS | 
            self.patterns.DESCRIPTIVE_WORDS | 
            self.patterns.COUNTRIES
        )
        
        # Find meaningful words (working backwards)
        for word in reversed(words):
            word_clean = re.sub(r'[^\w]', '', word.lower())
            if len(word_clean) > 2 and word_clean not in exclude_words:
                return word
        
        # Fallback to original name
        return name.strip()


class OriginExtractor:
    # Extracts product origin from name

    def __init__(self, patterns: ExtractionPatterns):
        # Initialize extractor with patterns
        self.patterns = patterns
        self.country_regex = re.compile(
            patterns.get_country_pattern(), 
            re.IGNORECASE
        )
    
    def extract_origin(self, name: str) -> Optional[str]:
        # Extract origin from product name
        match = self.country_regex.search(name.lower())
        if match:
            origin = match.group(1).title()
            # Normalize "Local" to "Saudi"
            if origin.lower() == "local":
                return "Saudi"
            return origin
        return None


class UnitExtractor:
    # Extracts product units from name

    def __init__(self, patterns: ExtractionPatterns):
        # Initialize extractor with patterns
        self.patterns = patterns
        self.unit_regex = re.compile(
            patterns.get_unit_pattern(), 
            re.IGNORECASE
        )
        # Special compound units
        self.compound_units = re.compile(
            r'\b(small box|medium box|large box|small bag|medium bag|large bag|'
            r'big bag|thermo box|tray pack|family pack)\b',
            re.IGNORECASE
        )
    
    def extract_unit(self, name: str) -> str:
        # Extract unit from product name
        # Check for compound units first
        match = self.compound_units.search(name.lower())
        if match:
            return match.group(0).strip()
        
        # Check for standard units
        match = self.unit_regex.search(name.lower())
        if match:
            return match.group(0).strip()
        
        return "1 piece"

