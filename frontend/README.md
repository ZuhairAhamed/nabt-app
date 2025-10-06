# Nabt Product Extractor - Frontend

A Streamlit-based web interface for the Nabt Product Extractor API.

## Features

### 🏠 Home Dashboard
- Quick navigation to all features
- API health status monitoring
- Overview of system capabilities

### ⚙️ Process Products
- Process daily product data files
- Extract and classify products using hybrid ML
- View processing statistics and results
- Monitor classification breakdown by method and category

### 🔍 Product Comparison
- Compare prices for specific products across suppliers
- View price statistics and visualizations
- Identify best deals and price ranges
- Interactive search with filters

### 📊 All Comparisons
- View all products with multiple suppliers
- Filter by category and minimum supplier count
- Export comparison data to CSV
- Comprehensive price analysis

### 📈 Price Trends
- Analyze historical price trends
- Compare multiple suppliers over time
- View price statistics and insights
- Identify optimal buying periods
- Export trend data for further analysis

### 🏆 Best Suppliers by Category
- Find most cost-effective suppliers per category
- View savings potential and performance metrics
- Compare supplier pricing across categories
- Export supplier analysis data

## Setup

### Prerequisites
- Python 3.8+
- FastAPI backend running on `http://localhost:8000` (or configure custom URL)

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Configuration

#### API URL
By default, the frontend connects to `http://localhost:8000`. To change this, modify the `base_url` in `app.py`:

```python
api_client = get_api_client(base_url="http://your-api-url:port")
```

## Project Structure

```
frontend/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── pages/                      # Page modules
│   ├── __init__.py
│   ├── process_products.py     # Process products page
│   ├── product_comparison.py   # Product comparison page
│   ├── all_comparisons.py      # All comparisons page
│   ├── price_trends.py         # Price trends page
│   └── best_suppliers.py       # Best suppliers page
└── utils/                      # Utility modules
    ├── __init__.py
    └── api_client.py           # API client wrapper
```

## Usage Guide

### Processing Products

1. Navigate to "Process Products" from the sidebar
2. Click "Start Processing" to process today's data file
3. View results including:
   - Total products processed
   - Success/error counts
   - Classification breakdown
   - Processing time

### Comparing Product Prices

1. Navigate to "Product Comparison"
2. Enter product name and unit (e.g., "Tomato", "kg")
3. Select time period (today/week/month)
4. Click "Compare Prices"
5. View price comparison across suppliers with visualizations

### Viewing All Comparisons

1. Navigate to "All Comparisons"
2. Filter by category (optional)
3. Set minimum number of suppliers
4. Select time period
5. Click "Load Comparisons"
6. Download data as CSV for further analysis

### Analyzing Price Trends

1. Navigate to "Price Trends"
2. Enter product name and unit
3. Optionally filter by supplier
4. Select number of days to analyze
5. Click "View Trends"
6. View line charts and statistics
7. Get insights on best buying times

### Finding Best Suppliers

1. Navigate to "Best Suppliers by Category"
2. Select analysis period (today/week/month)
3. Click "Load Best Suppliers"
4. View best supplier for each category
5. Analyze savings potential
6. Export detailed analysis

## API Integration

The frontend communicates with the FastAPI backend through the `APIClient` class in `utils/api_client.py`. All API endpoints are wrapped with error handling and timeout management.

### Available Endpoints

- `GET /health` - API health check
- `POST /api/process` - Process products
- `GET /api/comparison/product` - Get product comparison
- `GET /api/comparison/all` - Get all comparisons
- `GET /api/comparison/trends` - Get price trends
- `GET /api/comparison/categories/best` - Get best suppliers by category

## Troubleshooting

### API Connection Issues
- Ensure the FastAPI backend is running
- Check the API URL configuration
- Verify network connectivity
- Check firewall settings

### Data Not Loading
- Verify data files exist in the expected location
- Check MongoDB connection in backend
- Ensure products have been processed
- Try different time periods

### Performance Issues
- Reduce the number of days for trend analysis
- Filter by specific categories
- Clear browser cache
- Restart the Streamlit app

## Development

### Adding New Pages

1. Create a new file in `pages/` directory
2. Implement a `render(api_client)` function
3. Add the page to `pages/__init__.py`
4. Add navigation option in `app.py`

### Modifying Styles

Custom CSS is defined in `app.py` using `st.markdown()` with `unsafe_allow_html=True`.

## License

Part of the Nabt Product Extractor project.
