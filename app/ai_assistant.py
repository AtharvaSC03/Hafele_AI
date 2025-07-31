import os
import google.generativeai as genai
from PIL import Image
import tempfile
import pymysql
import pandas as pd

# --- Gemini API Key ---
from dotenv import load_dotenv

load_dotenv()  # Load from .env

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# --- Load Gemini Model ---
model = genai.GenerativeModel("models/gemini-1.5-flash")

# --- MySQL Database Connection ---
def fetch_hafele_products():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="hafele_catalog",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            results = cursor.fetchall()
            return pd.DataFrame(results)
    except Exception as e:
        print("❌ DB Error:", e)
        return pd.DataFrame(columns=["id", "product_name", "sku", "category", "description", "image_url", "Room Type", "Themes"])

# --- Product Matching Logic ---
def match_hafele_products(ai_text, room_type, theme):
    hafele_catalog = fetch_hafele_products()
    matched = []
    ai_text_lower = ai_text.lower()

    for _, row in hafele_catalog.iterrows():
        # Match room type exactly
        if str(row.get("Room Type", "")).strip().lower() != str(room_type).strip().lower():
            continue

        # Match theme partially
        row_theme = str(row.get("Themes", "")).strip().lower()
        if theme.strip().lower() not in row_theme:
            continue

        tags = " ".join([
            str(row["product_name"]),
            str(row["description"]),
            str(row["category"]),
            row_theme
        ]).lower()

        if any(tag in ai_text_lower for tag in tags.split()):
            matched.append(f"- 🧩 **{row['product_name']}** (SKU: `{row['sku']}`)")

    if matched:
        return "\n\n📦 **Matched Hafele Products for your style:**\n" + "\n".join(set(matched))
    return ""

# --- Main AI Recommendation Function ---
def generate_ai_recommendations(room_type, theme, description, uploaded_file=None):
    prompt = f"""
You are a Hafele interior design AI assistant. Please reply in a minimal, modern, friendly tone that delights the customer and sells the product.

🎯 Goal:
- 🛏️ Room Type: {room_type}
- 🎨 Interior Theme: {theme}
- 📝 User's Need: {description}

You are speaking to a customer in a Hafele showroom or online consultation. Help them imagine their dream space, using modern language, descriptive visuals, and emojis to make it fun and inspiring.

✨ Tone: Be creative, confident, visual — like a pro interior designer who is excited to help! Add emojis at the start of every section. Use language that makes the customer *feel* the transformation.

If an image is uploaded:
1. 🔍 Look for layout dimensions like “600mm”, “7ft”, etc., to determine scale.
2. 🧱 Identify furniture zones (e.g., base cabinets, corners, tall units, wall-mounted spaces).
3. 🧰 Suggest Hafele products (e.g., soft-close drawers, magic corners, organizers, LED strip lighting) that *fit the layout*.
4. ✨ Describe **why** each suggestion makes their home feel more modern, smart, luxurious, or ergonomic.
5. ⚙️ Recommend smart fittings where applicable (e.g., pull-out corner units, sensor lighting, handleless fittings, soft-close hinges).
6. 👀 Detect visible hardware like hinges, shelves, handles, lighting, or room features (like stove, sink, mirror, wardrobe zones). Suggest suitable Hafele products accordingly.

🎁 Output Style:
- Add sections with icons like:
  🛋️ Smart Storage  
  💡 Lighting Ideas  
  🚪 Hardware & Hinges  
  🖼️ Final Design Vibe

- Make the suggestions **visually appealing** and user-friendly. Mention actual Hafele product ideas.
- Close the response with a modern catchphrase like:
  ✨ *Smart meets Style — That’s Hafele!*  
  or  
  🧩 *Designed for today, built for life.*

Only suggest Hafele products that are relevant — avoid generic or competitor mentions.
"""

    try:
        if uploaded_file:
            # Save uploaded image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            with Image.open(tmp_file_path) as img:
                img = img.convert("RGB")
                img.verify()

            image = Image.open(tmp_file_path).convert("RGB")

            # Gemini multimodal input with image
            response = model.generate_content(
                [
                    {
                        "role": "user",
                        "parts": [
                            {"text": prompt},
                            image
                        ]
                    }
                ]
            )
        else:
            # Gemini text-only input
            response = model.generate_content(
                [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ]
            )

        ai_text = response.text.strip()
        matches = match_hafele_products(ai_text, room_type, theme)

        return ai_text + "\n\n" + matches if matches else ai_text

    except Exception as e:
        return f"⚠️ Error analyzing input: {str(e)}"
