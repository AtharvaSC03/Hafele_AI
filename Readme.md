# 🧠 Hafele AI Interior Designer Tool

An intelligent layout analysis tool that suggests premium **Hafele hardware and accessories** using **AI + image understanding**.

> 👨‍💻 Built entirely by [Atharva Chavan]in 2025 as a smart interior product recommender for Hafele India.

---

## 🔍 Overview

This AI assistant helps customers and interior designers upload **photos or descriptions** of their **kitchens, wardrobes, or bathrooms**, and instantly get **tailored Hafele product suggestions**.

It uses:
- **Gemini 2.0 Flash** for vision + language AI
- A **real Hafele product catalog**
- Clean **Streamlit UI** for user interaction

---

## 🚀 Features

✨ **Image & Text Upload** – Upload your room photo or describe it in your words  
🧠 **AI Layout Understanding** – Gemini AI interprets space, style, and layout  
📦 **Hafele Product Matching** – AI filters a real Hafele catalog (CSV format)  
🎨 **Theme & Room Filter** – Match by `Room Type` (Kitchen, Wardrobe) + `Theme`  
🖼️ **Product Carousel** – Preview top product matches (with image + title)

---

## 🗂️ Project Structure

hafele_ai_assistant/
├── app/
│ ├── main.py # Streamlit frontend
│ ├── ai_assistant.py # Gemini Flash API integration
│ ├── product_recommender.py # CSV filtering logic
│ ├── utils.py # Image conversion, helpers
├── data/
│ └── hafele_products.csv # Real scraped Hafele product dataset
├── assets/
│ └── sample_images/ # Example room images
├── .env # Gemini API key
├── requirements.txt
└── README.md # This file 📝


---

## 🧪 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/hafele-ai-assistant.git
cd hafele-ai-assistant

# 2. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Gemini API key in .env
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 5. Launch the app
streamlit run app/main.py
🧠 How the AI Works
The assistant sends prompts like this to Gemini Flash:

You are a Hafele product expert. Based on the uploaded room photo or user text, suggest 5 suitable Hafele products. Consider the room type and theme, and explain each choice in 3–4 lines.
Gemini returns a markdown-based response with product names, categories, and reasoning — which is then matched to the real catalog.

🖼️ Sample Input & Output
Upload Image (Kitchen)	AI Suggested Products
- Loox LED Recess Light
- Corner Drawer Organizer
- Soft-Close Runner

📦 Product CSV Sample

Product Name,Category,Room Type,Themes,SKU,ImageURL
Loox LED 4004 Recess 350mA,Lighting,Kitchen,Smart,833.72.440,https://hafele.com/images/led.jpg
SlideOn Soft-close Drawer,Drawers,Wardrobe,Premium,433.02.250,https://hafele.com/images/drawer.jpg
...
📌 To-Do & Enhancements
 Admin Panel to Add/Edit Products

 Pricing + Quote Builder

 User Login & Save Designs

 Prebuilt Hafele Layout Packs

🧑‍💻 Creator Info
Atharva Chavan
💼 Full-stack AI Developer
🔗 LinkedIn | GitHub

📄 License
This project is released under the MIT License.