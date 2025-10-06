"""
Nabt Product Extractor - Streamlit Frontend
Main application entry point with navigation
"""
import streamlit as st
from utils.api_client import get_api_client

# Page configuration
st.set_page_config(
    page_title="Nabt Product Extractor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default Streamlit page navigation
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E7D32;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E7D32;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize API client
api_client = get_api_client()

# Sidebar navigation
st.sidebar.title("🌱 Nabt")
st.sidebar.markdown("---")

# API Health Check in sidebar
with st.sidebar:
    st.subheader("API Status")
    health = api_client.health_check()
    if health["status"] == "success":
        st.success("✅ Connected")
    else:
        st.error("❌ Disconnected")
        st.caption(f"Error: {health.get('message', 'Unknown error')}")

st.sidebar.markdown("---")

# Navigation menu
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "⚙️ Process Products",
        "🔍 Product Comparison"
    ]
)


# Main content area
if page == "🏠 Home":
    st.markdown('<div class="main-header">🌱 Nabt Product Extractor</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Product Extraction and Classification System</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ⚙️ Process Products")
        st.write("Extract and classify products from raw data files using hybrid ML approach.")
        if st.button("Go to Process Products", key="nav_process"):
            st.rerun()

    with col2:
        st.markdown("### 🔍 Compare Prices")
        st.write("Compare product prices across different suppliers and find the best deals.")
        if st.button("Go to Comparisons", key="nav_compare"):
            st.rerun()

    st.markdown("---")

    st.markdown("## 🚀 Quick Start")
    st.markdown("""
    1. **Process Products**: Upload or process daily product data files
    2. **Compare Prices**: Find the best prices across suppliers
    """)

    st.markdown("## 🛠️ Features")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Hybrid ML Approach")
        st.write("- Regex patterns for simple products")
        st.write("- LLM fallback for complex items")
        st.write("- Automatic classification into 16 categories")

    with col2:
        st.markdown("#### Price Intelligence")
        st.write("- Multi-supplier price comparison")
        st.write("- Detailed product statistics")
        st.write("- Best price identification")

elif page == "⚙️ Process Products":
    from pages import process_products
    process_products.render(api_client)

elif page == "🔍 Product Comparison":
    from pages import product_comparison
    product_comparison.render(api_client)