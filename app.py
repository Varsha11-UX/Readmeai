# app.py

import streamlit as st
import os
import base64
#from dotenv import load_dotenv
from utils.recommender import get_books_by_genre
from utils.chatbot import ask_reading_buddy

#load_dotenv()

# -------------------------------
# Page Setup
# -------------------------------
st.set_page_config(page_title="ReadWise AI", page_icon="📚", layout="wide")

# -------------------------------
# Set Background
# -------------------------------
def set_background(image_file, selector=".stApp"):
    with open(image_file, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    {selector} {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("static/light_bg.png")

# -------------------------------
# Theme toggle
# -------------------------------
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

# -------------------------------
# Column background CSS
# -------------------------------
def add_section_backgrounds():
    with open("static/recommendation_bg.png", "rb") as f:
        rec_b64 = base64.b64encode(f.read()).decode()
    with open("static/chatbot_bg.png", "rb") as f:
        chat_b64 = base64.b64encode(f.read()).decode()

    overlay = "rgba(255,255,255,0.5)" if theme == "Light" else "rgba(0,0,0,0.4)"
    color = "#111" if theme == "Light" else "#fff"

    st.markdown(f"""
    <style>
    .tab-section {{
        background-size: cover;
        background-position: center;
        border-radius: 12px;
        padding: 2rem;
        position: relative;
        color: {color};
    }}
    .rec-tab {{ background-image: url("data:image/png;base64,{rec_b64}"); }}
    .chat-tab {{ background-image: url("data:image/png;base64,{chat_b64}"); }}
    .tab-section::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: {overlay};
        border-radius: 12px;
        z-index: 0;
    }}
    .tab-section * {{ z-index: 1; position: relative; }}
    </style>
    """, unsafe_allow_html=True)

add_section_backgrounds()

# -------------------------------
# Banner
# -------------------------------
st.markdown(f"""
<div style="
    background: linear-gradient(90deg, #ff914d, #ffcd8c);
    border-radius: 15px;
    padding: 40px 20px;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
">
    <h1 style="font-size: 3em;">📚 ReadWise AI</h1>
    <p style="font-size: 1.2em;">
        Discover books that match your mood. Ask anything. Buy smarter.<br>
        Your cozy AI-powered reading nook awaits.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📖 Recommendations", "🤖 Reading Buddy", "🛍️ Buy Smart"])

# ---------------------------------
# 📖 Recommendations Tab
# ---------------------------------
with tab1:
    st.markdown('<div class="tab-section rec-tab">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        mood = st.text_input("💭 I'm feeling...", placeholder="e.g., curious, joyful")
    with col2:
        genre = st.text_input("🎯 I like this genre...", placeholder="e.g., sci-fi, history")

    if st.button("🔍 Get Book Recommendations"):
        query = mood or genre
        if not query:
            st.warning("Please enter a mood or genre.")
        else:
            with st.spinner("🔎 Finding books..."):
                books = get_books_by_genre(query)
            if not books:
                st.error("😕 No results. Try a different mood or genre.")
            else:
                for book in books:
                    with st.container():
                        cols = st.columns([1, 3])
                        with cols[0]:
                            thumbnail = book.get("thumbnail", "https://via.placeholder.com/100x150")
                            st.image(thumbnail, width=100)
                        with cols[1]:
                            st.subheader(book["title"])
                            st.write("👩‍💻 **Authors:**", ", ".join(book["authors"]))
                            st.write("📝 " + book["description"])
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------
# 🤖 Reading Buddy Tab
# ---------------------------------
with tab2:
    st.markdown('<div class="tab-section chat-tab">', unsafe_allow_html=True)
    st.markdown("### Ask our intelligent reading buddy anything!")

    user_input = st.text_area("💬 Ask about books, quotes, or topics...")
    if st.button("🎙️ Get Response"):
        if user_input:
            with st.spinner("💡 Thinking..."):
                response = ask_reading_buddy(user_input)
                st.success(response)
        else:
            st.warning("Please type something first.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------
# 🛍️ Buy Smart Tab
# ---------------------------------
with tab3:
    st.markdown('<div class="tab-section rec-tab">', unsafe_allow_html=True)
    book_query = st.text_input("🔍 Search a book to buy...", placeholder="e.g., Atomic Habits")
    if book_query:
        title_encoded = book_query.replace(" ", "+")
        st.markdown(f"""
        #### Buy Links:
        - 🛍️ [Amazon](https://www.amazon.in/s?k={title_encoded})
        - 🛒 [Flipkart](https://www.flipkart.com/search?q={title_encoded})
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
# -------------------------------
# Surprise Me! Section (Centered + Styled)
# -------------------------------
import random

st.markdown("---")

# Center the container
st.markdown("""
<div style='text-align: center; padding: 30px; background-color: #f9f5f2; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
    <h2 style='color: #ff914d;'>🎁 Surprise Me!</h2>
""", unsafe_allow_html=True)

if st.button("✨ Click for a Surprise!", key="surprise_button", use_container_width=True):
    random_quotes = [
        "“A reader lives a thousand lives before he dies.” – George R.R. Martin",
        "“Books are a uniquely portable magic.” – Stephen King",
        "“Until I feared I would lose it, I never loved to read.” – Harper Lee",
        "“Reading gives us someplace to go when we have to stay where we are.” – Mason Cooley",
        "“That’s the thing about books. They let you travel without moving your feet.” – Jhumpa Lahiri"
    ]

    random_books = [
        "📖 *The Alchemist* by Paulo Coelho",
        "📖 *Sapiens* by Yuval Noah Harari",
        "📖 *Atomic Habits* by James Clear",
        "📖 *1984* by George Orwell",
        "📖 *To Kill a Mockingbird* by Harper Lee"
    ]

    random_poems = [
        "In quiet corners books do lie,<br>With tales that let the soul fly high.",
        "A turn of page, a twist, a start—<br>A story gently moves the heart.",
        "Books are lanterns in the dark,<br>Each word a glowing, guiding spark.",
        "A whisper of wisdom, a paper breeze—<br>In stories we find gentle peace.",
        "No passport needed, no loud crowd—<br>Just ink and dreams in pages proud."
    ]

    st.markdown(f"""
    <div style='margin-top: 20px;'>
        <p style='font-size: 1.2em;'><strong>📚 Quote:</strong><br>{random.choice(random_quotes)}</p>
        <p style='font-size: 1.1em;'><strong>📘 Book Pick:</strong><br>{random.choice(random_books)}</p>
        <p style='font-style: italic; font-size: 1.05em; color: #444;'>{random.choice(random_poems)}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
