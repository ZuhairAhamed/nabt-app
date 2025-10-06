"""
Product Comparison Page
Compare prices for a specific product across suppliers
"""
import streamlit as st
import pandas as pd


def render(api_client):
    # Render the product comparison page
    st.markdown("## 🔍 Product Comparison")
    st.markdown("Compare prices for a specific product across all suppliers.")

    st.markdown("---")

    # Input form
    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input(
            "Product Name",
            placeholder="e.g., Apple, Tomato, Milk",
            help="Enter the product name to compare (partial name matching supported)"
        )

    with col2:
        period = st.selectbox(
            "Period",
            ["today", "week", "month", "quarter", "year", "all"],
            help="Select the time period for comparison"
        )

    # Search button
    search_btn = st.button("🔍 Compare Prices", type="primary", use_container_width=True)

    if search_btn:
        if not product_name:
            st.warning("⚠️ Please enter a product name.")
        else:
            with st.spinner("Fetching price comparison..."):
                result = api_client.get_product_comparison(product_name, period)

            if result["status"] == "success":
                data = result["data"]

                # Display product info
                st.markdown("### 📦 Product Information")
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Product", data.get("product_name", "N/A"))

                with col2:
                    st.metric("Category", data.get("category", "N/A"))

                # Supplier prices
                if data.get("supplier_prices"):
                    st.markdown("### 💰 Price Comparison")

                    prices = data["supplier_prices"]
                    df = pd.DataFrame(prices)

                    # Add unit column
                    unit_value = data.get("unit", "N/A")
                    df["unit"] = unit_value

                    # Sort by price
                    df = df.sort_values("price")

                    # Reorder columns to show: supplier, price, currency, unit, date
                    column_order = ["supplier", "price", "currency", "unit", "date"]
                    df = df[column_order]

                    # Display as table
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Best price highlight
                    if len(prices) > 0:
                        best_price = prices[0]
                        st.success(
                            f"🏆 **Best Price**: {best_price['supplier']} - "
                            f"{best_price['price']} {best_price.get('currency', 'SAR')}"
                        )

                    # Price range
                    if len(prices) > 1:
                        price_range = prices[-1]["price"] - prices[0]["price"]
                        st.info(
                            f"📊 **Price Range**: {price_range:.2f} {prices[0].get('currency', 'SAR')} "
                            f"(from {prices[0]['price']:.2f} to {prices[-1]['price']:.2f})"
                        )

                else:
                    st.info("No supplier prices found for this product.")

                # Statistics
                if data.get("statistics"):
                    st.markdown("### 📈 Statistics")
                    stats = data["statistics"]

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Average Price", f"{stats.get('avg_price', 0):.2f}")

                    with col2:
                        st.metric("Lowest Price", f"{stats.get('min_price', 0):.2f}")

                    with col3:
                        st.metric("Highest Price", f"{stats.get('max_price', 0):.2f}")

                    with col4:
                        st.metric("Suppliers", stats.get("supplier_count", 0))

                # Savings Opportunity
                if data.get("potential_savings_amount", 0) > 0:
                    st.markdown("### 💡 Savings Opportunity")
                    savings_pct = data.get("potential_savings_pct", 0)
                    savings_amount = data.get("potential_savings_amount", 0)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Potential Savings", f"{savings_amount:.2f} SAR", delta=f"{savings_pct:.1f}%")
                    with col2:
                        best = data.get("best_price_supplier", "N/A")
                        worst = data.get("worst_price_supplier", "N/A")
                        st.info(f"💡 Switch from **{worst}** to **{best}** to save {savings_pct:.1f}%")

            else:
                st.error(f"❌ Error: {result.get('message', 'Unknown error')}")

    # Example products
    with st.expander("💡 Example Products", expanded=False):
        st.markdown("""
        Try searching for these common products:
        - **Apple** - Fresh apples
        - **Tomato** - Fresh tomatoes
        - **Milk** - Dairy milk
        - **Chicken** - Fresh chicken
        - **Cucumber** - Fresh cucumbers

        Note: The API supports partial name matching, so you can search for "app" to find "apple" products.
        """)