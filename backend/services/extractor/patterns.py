"""
Extraction patterns for product data.
"""

from dataclasses import dataclass, field
from typing import Set


@dataclass
class ExtractionPatterns:
    # Regex patterns and keywords for product data extraction
    
    COUNTRIES: Set[str] = field(default_factory=lambda: {
        'local', 'philippines', 'egypt', 'saudi', 'saudi arabia', 'china', 
        'tunisia', 'south africa', 'spain', 'tanzania', 'italy', 'usa', 
        'united states', 'brazil', 'india', 'turkey', 'lebanon', 'jordan', 
        'morocco', 'france', 'germany', 'netherlands', 'uk', 'uae', 'qatar',
        'bahrain', 'kuwait', 'oman', 'yemen', 'pakistan', 'bangladesh',
        'thailand', 'vietnam', 'malaysia', 'indonesia', 'australia'
    })
    
    UNIT_KEYWORDS: Set[str] = field(default_factory=lambda: {
        'kg', 'g', 'gram', 'grams', 'kilogram', 'kilograms',
        'lb', 'pound', 'pounds', 'lbs', 'oz', 'ounce', 'ounces',
        'liter', 'l', 'litre', 'liters', 'litres', 'ml',
        'pkt', 'packet', 'packets', 'bunch', 'bunches',
        'box', 'boxes', 'bag', 'bags', 'piece', 'pieces', 'pcs',
        'dozen', 'dozens', 'bundle', 'bundles', 'head', 'heads',
        'bottle', 'bottles', 'can', 'cans', 'tin', 'tins',
        'jar', 'jars', 'tube', 'tubes', 'roll', 'rolls',
        'sheet', 'sheets', 'slice', 'slices', 'pack', 'packs',
        'tray', 'unit', 'units'
    })
    
    DESCRIPTIVE_WORDS: Set[str] = field(default_factory=lambda: {
        # Quality descriptors
        'farm', 'fresh', 'organic', 'premium', 'natural', 'sustainable',
        'quality', 'grade', 'type', 'variety', 'brand', 'deluxe',
        'luxury', 'gourmet', 'artisanal', 'handcrafted', 'homemade',
        'traditional', 'authentic', 'genuine', 'pure',
        # Size descriptors
        'small', 'medium', 'large', 'extra', 'super', 'mega', 'jumbo',
        'mini', 'baby', 'big', 'thermo',
        # State descriptors
        'ripe', 'raw', 'cooked', 'frozen', 'dried', 'freshly',
        'locally', 'grown', 'harvested', 'picked', 'selected',
        # Color descriptors
        'red', 'green', 'yellow', 'orange', 'purple', 'blue',
        'white', 'black', 'brown', 'pink', 'golden',
        # Apple varieties (keep specific if needed, otherwise remove)
        'royal', 'gala', 'fuji', 'granny', 'smith', 'honeycrisp',
        'delicious', 'lady', 'braeburn'
    })
    
    COMPLEXITY_KEYWORDS: Set[str] = field(default_factory=lambda: {
        'organic', 'premium', 'fresh', 'natural', 'sustainable',
        'fair-trade', 'quality', 'grade', 'type', 'variety', 'brand'
    })
    
    def get_country_pattern(self) -> str:
        # Get regex pattern for country extraction
        countries_str = '|'.join(sorted(self.COUNTRIES, key=len, reverse=True))
        return rf'\b({countries_str})\b'
    
    def get_unit_pattern(self) -> str:
        # Get regex pattern for unit extraction
        units_str = '|'.join(sorted(self.UNIT_KEYWORDS, key=len, reverse=True))
        return rf'\b(\d+(?:\.\d+)?)\s*({units_str})\b'
    
    def get_descriptive_pattern(self) -> str:
        # Get regex pattern for descriptive words
        words_str = '|'.join(sorted(self.DESCRIPTIVE_WORDS, key=len, reverse=True))
        return rf'\b({words_str})\b'

