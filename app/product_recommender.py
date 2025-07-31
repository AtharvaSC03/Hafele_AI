# app/product_recommender.py

import pandas as pd

def filter_products(df, room_type, theme):
    """
    Filter the Hafele product catalog based on room type and theme.

    Args:
        df (DataFrame): Hafele catalog from MySQL.
        room_type (str): e.g. Kitchen, Wardrobe
        theme (str): e.g. Modern, Rustic

    Returns:
        DataFrame: Top matching filtered products (up to 10).
    """
    # Ensure required columns exist
    if "Room Type" not in df.columns or "Themes" not in df.columns:
        return pd.DataFrame()  # Return empty if something's wrong

    # Lowercase string matching for flexible filters
    room_filter = df["Room Type"].astype(str).str.lower().str.contains(room_type.lower())
    theme_filter = df["Themes"].astype(str).str.lower().str.contains(theme.lower())

    filtered = df[room_filter & theme_filter]

    # Limit to top 10 results
    return filtered.head(10) if len(filtered) > 10 else filtered
