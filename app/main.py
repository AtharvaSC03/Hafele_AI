import streamlit as st
import pandas as pd
import mysql.connector
from ai_assistant import generate_ai_recommendations
from product_recommender import filter_products

# --- MySQL DB connection ---
def load_catalog_from_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Change this if you set a MySQL password
            database="hafele_catalog"
        )
        query = "SELECT * FROM products;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        return pd.DataFrame()

# Load Hafele product catalog from MySQL
catalog_df = load_catalog_from_db()

# --- Streamlit UI ---
st.set_page_config(page_title="Hafele Interior Designer AI", layout="wide")
st.title("🎨 Hafele Interior Designer Tool")
st.markdown("Upload your room layout and get AI-powered Hafele product suggestions based on space and style.")

# --- User Inputs ---
room_type = st.selectbox("🏠 Select Room Type", ["Kitchen", "Wardrobe", "Bathroom", "Living Room"])
theme = st.selectbox("🎨 Choose Interior Theme", ["Modern", "Classic", "Minimalist", "Rustic", "Industrial"])
description = st.text_area("📝 Describe your layout, needs, or any existing hardware", placeholder="e.g., L-shaped kitchen with corner cabinets and overhead lighting...")
uploaded_file = st.file_uploader("📸 Upload room layout photo (optional)", type=["jpg", "jpeg", "png"])

# --- Button + AI Response ---
if st.button("🔍 Get Hafele AI Recommendations"):
    with st.spinner("Thinking like a Hafele design expert..."):
        ai_response = generate_ai_recommendations(room_type, theme, description, uploaded_file)
        filtered_products = filter_products(catalog_df, room_type, theme)

        # AI Suggestions
        st.subheader("🧠 AI Design Suggestions")
        st.write(ai_response)

        # Carousel
        if not filtered_products.empty:
            st.subheader("🖼️ Top 5 Product Carousel")
            top_5 = filtered_products.head(5)
            cols = st.columns(len(top_5))
            for i, row in enumerate(top_5.itertuples()):
                with cols[i]:
                    if getattr(row, "image_url", "").startswith("http"):
                        st.image(getattr(row, "image_url"), use_column_width=True)
                    st.caption(f"**{getattr(row, 'product_name', 'No Name')}**")
                    st.caption(f"💡 {getattr(row, 'category', '')} | 🆔 {getattr(row, 'sku', '')}")

        st.markdown("---")
        st.subheader("🛠️ Full Matching Hafele Products")

        # Full List
        for _, row in filtered_products.iterrows():
            st.markdown(f"**{row.get('product_name', 'No Product Name')}**")
            if pd.notna(row.get('image_url', '')) and row['image_url'].startswith("http"):
                st.image(row['image_url'], width=300)
            st.markdown(
                f"{row.get('description', 'No Description')}  \n"
                f"💡 Category: {row.get('category', 'N/A')}  \n"
                f"🆔 SKU: `{row.get('sku', 'N/A')}`"
            )
            st.markdown("---")
        if filtered_products.empty:
            st.warning("No matching Hafele products found for the selected filters.")
