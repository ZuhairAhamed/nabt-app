"""
Process Products Page
Trigger product extraction and classification
"""
import streamlit as st
from datetime import datetime


def render(api_client):
    """Render the process products page."""
    st.markdown("## ⚙️ Process Products")
    st.markdown("Extract and classify products from today's data file using hybrid ML approach.")

    st.markdown("---")

    # Information section
    with st.expander("ℹ️ How It Works", expanded=False):
        st.markdown("""
        ### Processing Pipeline
        1. **Load Data**: Reads `data-DD-MM-YYYY.json` from the data directory
        2. **Extract Information**: Uses regex patterns for simple products, LLM for complex ones
        3. **Classify Products**: Rule-based classification with LLM fallback
        4. **Save Results**: Stores in MongoDB and generates output JSON file

        ### What Gets Extracted
        - Product Name
        - Origin
        - Brand
        - Unit (kg, liter, etc.)
        - Price
        - Category (16 categories available)
        - Classification confidence
        """)

    # Process button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        process_btn = st.button(
            "🚀 Start Processing",
            type="primary",
            use_container_width=True
        )

    if process_btn:
        with st.spinner("Processing products... This may take a few minutes."):
            result = api_client.process_products()

        if result["status"] == "success":
            st.success("✅ Processing completed successfully!")
        else:
            st.error(f"❌ Error: {result.get('message', 'Unknown error')}")