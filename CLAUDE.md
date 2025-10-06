# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nabt is a product extraction and classification system that processes raw product data using a hybrid ML approach (regex patterns + LLM fallback). It extracts structured product information and classifies items into categories, then stores results in MongoDB.

## Development Commands

### Environment Setup
```bash
# Copy environment template and configure
cp .env.example .env
# Edit .env to add GROQ_API_KEY and MongoDB settings

# Install dependencies (using uv)
uv sync
```

### Running the Application
```bash
# Start the FastAPI server
python -m uvicorn api.main:app --reload

# Or run directly
python src/api/main.py

# Access API docs at http://localhost:8000/docs
```

### Testing and Quality
```bash
# Run tests
pytest

# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

## Architecture

### Hybrid Processing Pipeline

The system uses a two-tier hybrid approach for both extraction and classification:

**Extraction Flow** (src/services/extractor/product_extractor.py):
1. Complexity check determines routing
2. Simple products → regex patterns (patterns.py) + cleaners (cleaners.py)
3. Complex products → LLM extraction with fallback to regex
4. Complexity indicators: >5 words, special chars, >50 chars, complexity keywords

**Classification Flow** (src/services/classifier/product_classifier.py):
1. Rule-based classifier runs first (keyword matching with scoring)
2. High confidence (>0.85) → use rule-based result
3. Low confidence + LLM available → LLM classification
4. Fallback to rule-based if LLM fails

### Key Components

**HybridProductExtractor** (src/services/extractor/product_extractor.py):
- Entry point: `extract_product_data(raw_data)`
- Decides between `_extract_with_regex()` and `_extract_with_llm()`
- Extracts: ProductName, Origin, Brand, Unit, Price
- Passes to classifier for category assignment

**HybridProductClassifier** (src/services/classifier/product_classifier.py):
- Entry point: `classify_product(product_name)`
- RuleBasedClassifier: keyword scoring with position/length weighting
- LLM fallback for confidence ≤0.85
- Returns: category, confidence, method

**ProductService** (src/services/product_service.py):
- Orchestrates: load data → extract → classify → save to file + MongoDB
- `process_daily_products()` expects files: `data/data-DD-MM-YYYY.json`
- Generates output: `test_data_DD-MM-YYYY.json`

### Data Flow

```
Raw JSON (data/data-DD-MM-YYYY.json)
    ↓
ProductService.load_data_file()
    ↓
HybridProductExtractor.extract_product_data()
    ├→ Regex extraction (simple) OR LLM extraction (complex)
    ↓
HybridProductClassifier.classify_product()
    ├→ Rule-based (high confidence) OR LLM (low confidence)
    ↓
Product model (validated)
    ↓
MongoDB + JSON output file
```

### Configuration

Settings are managed via environment variables (loaded in src/core/config.py):
- GROQ_API_KEY: Required for LLM features
- MONGODB_URI/DATABASE/COLLECTION: Database connection
- DATA_DIRECTORY: Location of input files (defaults to `data/`)
- LLM availability checked at runtime - system degrades gracefully to regex-only if unavailable

### API Structure

**FastAPI App** (src/api/main.py):
- POST /process: Processes today's data file from DATA_DIRECTORY
- GET /health: Health check
- Routes defined in src/api/routes.py
- Schemas (request/response models) in src/api/schemas.py

### LLM Integration

**Configuration** (src/llm/config.py):
- Uses ChatGroq with Groq API
- `is_llm_available()` checks for valid API key
- Temperature: 0 for extraction, 0.1 for classification

**Prompts** (src/llm/prompts.py):
- `create_extraction_prompt()`: Structured extraction with Pydantic output parser
- `create_classification_prompt()`: Category classification from predefined list

### Product Categories

16 categories defined in src/services/classifier/categories.py:
- Food: Fruits, Vegetables, Herbs, Grains, Legumes, Nuts, Spices, Dairy, Meat, Seafood
- Packaged: Beverages, Snacks, Bakery, Frozen, Canned
- Other: Catchall for unmatched items

Each category has extensive keyword lists including English terms and transliterations.

## Important Implementation Notes

### When Adding New Categories
1. Update ProductCategory enum in src/services/classifier/categories.py
2. Add keyword mappings in get_category_keywords()
3. Update LLM classification prompt in src/llm/prompts.py to include new category

### When Modifying Extraction Patterns
- Patterns centralized in src/services/extractor/patterns.py
- Cleaners in src/services/extractor/cleaners.py use these patterns
- Update complexity indicators in HybridProductExtractor._is_complex_product_name() if needed

### MongoDB Schema
Products stored with fields: date, name, origin, brand, unit, price, currency, source, category, confidence, classification_method, original_name
- Indexes: (date, name) and (date, source)
- Date format: YYYY-MM-DD
- Service uses singleton pattern: get_mongo_service()

### Input Data Format
Expected JSON structure:
```json
{
  "data": [
    {
      "name": "Product name with details",
      "price": "12.50",
      "source": "provider_name"
    }
  ]
}
```

### Error Handling
- ProductService collects errors per product (doesn't fail entire batch)
- LLM failures gracefully fallback to regex
- MongoDB errors logged but raised (no silent failures)