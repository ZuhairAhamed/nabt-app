"""
Prompt Templates for LLM Operations
Contains all prompt templates used for classification and data extraction.
"""

from langchain.prompts import ChatPromptTemplate


class ProductClassificationPrompts:
    # Prompt templates for product classification
    
    CATEGORIES = """Categories:
    - Fruits: Apples, bananas, oranges, berries, etc.
    - Vegetables: Tomatoes, carrots, onions, leafy greens, etc.
    - Herbs: Basil, parsley, mint, oregano, etc.
    - Grains: Rice, wheat, oats, quinoa, etc.
    - Legumes: Beans, lentils, chickpeas, peas, etc.
    - Nuts: Almonds, walnuts, cashews, seeds, etc.
    - Spices: Pepper, cinnamon, turmeric, etc.
    - Dairy: Milk, cheese, yogurt, butter, etc.
    - Meat: Beef, chicken, pork, lamb, etc.
    - Seafood: Fish, shrimp, crab, etc.
    - Beverages: Juice, soda, water, tea, coffee, etc.
    - Snacks: Chips, crackers, nuts, candy, etc.
    - Bakery: Bread, cakes, pastries, etc.
    - Frozen: Frozen vegetables, fruits, meals, etc.
    - Canned: Canned goods, preserves, etc.
    - Other: Anything that doesn't fit above categories"""
    
    CLASSIFICATION_RULES = """Rules:
    1. Focus on the main product type, ignore packaging details
    2. Consider Arabic and English product names
    3. Be consistent with similar products
    4. If unsure, choose the most likely category

    Respond with only the category name (e.g., "Fruits")."""
    
    @staticmethod
    def get_system_prompt() -> str:
        # Get the system prompt for classification
        return f"""You are a product classification expert. Classify products into these categories:

        {ProductClassificationPrompts.CATEGORIES}

        {ProductClassificationPrompts.CLASSIFICATION_RULES}"""
            
    @staticmethod
    def get_template() -> ChatPromptTemplate:
        # Create a prompt template for product classification
        return ChatPromptTemplate.from_messages([
            ("system", ProductClassificationPrompts.get_system_prompt()),
            ("human", "Classify this product: {product_name}")
        ])


class ProductExtractionPrompts:
    # Prompt templates for product data extraction
    
    EXTRACTION_RULES = """Rules:
    - Original_name: Keep as provided
    - ProductName: Extract ONLY the core product name (e.g., "Tomato" from "Farm Fresh Bunch Tomato 500g")
    Remove all descriptive words like: Farm, Fresh, Organic, Premium, Natural, Bunch, Bundle, Pack, Box, Bag, etc.
    Remove origin countries, units, weights, and packaging information
    Keep only the essential product name that identifies what the item actually is
    - Unit: Packaging/weight/size (e.g., "1 kg", "500 g", "1 bunch")
    - Origin: Country/label (e.g., "Local", "Philippines") or null
    - Price: Numeric value only (float)
    - Currency: Always "SAR"
    - Source: Keep as provided"""
        
    EXTRACTION_EXAMPLES = """Examples:
    - "Farm Fresh Bunch Tomato 500g" → ProductName: "Tomato"
    - "Organic Premium Apple Royal Gala China 1 kg" → ProductName: "Apple"
    - "Fresh Local Carrot Bunch" → ProductName: "Carrot"
    - "Premium Quality Banana Philippines 1 kg" → ProductName: "Banana"

    Return only valid JSON."""
    
    @staticmethod
    def get_system_prompt(format_instructions: str = "") -> str:
        # Get the system prompt for data extraction
        prompt = f"""You are a data extraction assistant. Extract product data into JSON format.

        {ProductExtractionPrompts.EXTRACTION_RULES}

        {ProductExtractionPrompts.EXTRACTION_EXAMPLES}"""
        
        if format_instructions:
            prompt += f"\n\n{format_instructions}"
        
        return prompt
    
    @staticmethod
    def get_template() -> ChatPromptTemplate:
        # Create a prompt template for product data extraction
        return ChatPromptTemplate.from_messages([
            ("system", ProductExtractionPrompts.get_system_prompt("{format_instructions}")),
            ("human", "Extract: Product='{name}', Price='{price}', Source='{source}'")
        ])


# Convenience functions for backward compatibility
def create_classification_prompt() -> ChatPromptTemplate:
    # Create a classification prompt template
    return ProductClassificationPrompts.get_template()


def create_extraction_prompt() -> ChatPromptTemplate:
    # Create an extraction prompt template
    return ProductExtractionPrompts.get_template()

