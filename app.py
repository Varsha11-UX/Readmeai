import streamlit as st
import base64
import random
from utils.recommender import get_books_by_genre
from utils.chatbot import ask_reading_buddy

# Page setup
st.set_page_config(page_title="ReadWise AI", page_icon="📚", layout="wide")

# Full-page background
def set_background(image_file):
    with open(image_file, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """, unsafe_allow_html=True)

set_background("static/light_bg.png")

# Section backgrounds
def add_section_backgrounds():
    with open("static/recommendation_bg.png", "rb") as f:
        rec_b64 = base64.b64encode(f.read()).decode()
    with open("static/chatbot_bg.png", "rb") as f:
        chat_b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .tab-section {{
        background-size: cover;
        background-position: center;
        border-radius: 12px;
        padding: 2rem;
        position: relative;
        color: white;
    }}
    .rec-tab {{ background-image: url("data:image/png;base64,{rec_b64}"); }}
    .chat-tab {{ background-image: url("data:image/png;base64,{chat_b64}"); }}
    .tab-section::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: rgba(0,0,0,0.4);
        border-radius: 12px;
        z-index: 0;
    }}
    .tab-section * {{ z-index: 1; position: relative; }}
    </style>
    """, unsafe_allow_html=True)

add_section_backgrounds()

# Header
st.markdown("""
<div style="background: linear-gradient(90deg, #ff914d, #ffcd8c); padding: 2rem; border-radius: 15px; text-align: center; color: white;">
    <h1>📚 ReadWise AI</h1>
    <p>Discover books that match your mood. Ask anything. Buy smarter.</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📖 Recommendations", "🤖 Chatbot", "🛍️ Buy Smart"])

# --- Tab 1: Recommendations ---
with tab1:
    st.markdown('<div class="tab-section rec-tab">', unsafe_allow_html=True)
    st.subheader("📖 Mood/Genre-Based Book Recommendations")
    query = st.text_input("Enter your mood or genre (e.g., happy, sci-fi, historical):")

    if st.button("🔍 Get Recommendations"):
        if not query:
            st.warning("Please enter something.")
        else:
            with st.spinner("Searching..."):
                books = get_books_by_genre(query)
            if not books:
                st.error("😕 No books found.")
            else:
                for book in books:
                    st.image(book["thumbnail"], width=100)
                    st.markdown(f"### {book['title']}")
                    st.markdown(f"**Authors:** {', '.join(book['authors'])}")
                    st.write(book["description"])
                    st.markdown(f"[More Info 📘]({book['info_link']})")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tab 2: Chatbot ---
with tab2:
    st.markdown('<div class="tab-section chat-tab">', unsafe_allow_html=True)
    st.subheader("🤖 Ask Your Reading Buddy")
    user_input = st.text_area("💬 Ask something about books, quotes, genres...")

    if st.button("🎙️ Ask Chatbot"):
        if user_input:
            with st.spinner("Thinking..."):
                reply = ask_reading_buddy(user_input)
            st.success(reply)
        else:
            st.warning("Please enter a message.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tab 3: Buy Smart ---
# --- Tab 3: Buy Smart ---
with tab3:
    st.markdown('<div class="tab-section rec-tab">', unsafe_allow_html=True)
    st.subheader("🛍️ Search to Buy a Book")

    title = st.text_input("Search by book title:", placeholder="e.g., Atomic Habits")

    if title:
        with st.spinner("Fetching book info..."):
            books = get_books_by_genre(title)

        if not books:
            st.warning("No book found.")
        else:
            book = books[0]  # show the top result
            st.image(book["thumbnail"], width=120)
            st.markdown(f"### {book['title']}")
            st.markdown(f"**Authors:** {', '.join(book['authors'])}")
            st.write(book["description"])

            encoded = title.replace(" ", "+")
            st.markdown("#### Buy Links:")
            st.markdown(f"- 🛍️ [Buy on Amazon](https://www.amazon.in/s?k={encoded})")
            st.markdown(f"- 🛒 [Buy on Flipkart](https://www.flipkart.com/search?q={encoded})")

    st.markdown('</div>', unsafe_allow_html=True)


# --- Surprise Me Section ---
# --- 💡 Book Blink Section ---

st.markdown("---")
st.markdown("<h2 style='text-align:center;'>💡 Book Blink</h2>", unsafe_allow_html=True)

if st.button("📖 Reveal a Random Blink!", key="surprise"):
    quotes = [
        "“A reader lives a thousand lives before he dies.” – George R.R. Martin",
        "“Books are a uniquely portable magic.” – Stephen King",
        "“Reading gives us someplace to go when we have to stay where we are.” – Mason Cooley"
    ]
    books = [
        "📖 *The Alchemist* by Paulo Coelho",
        "📖 *Sapiens* by Yuval Noah Harari",
        "📖 *1984* by George Orwell"
    ]
    poems = [
        "Books are lanterns in the dark,<br>Each word a glowing, guiding spark.",
        "A whisper of wisdom, a paper breeze—<br>In stories we find gentle peace."
    ]
    st.markdown(f"**📚 Quote:** {random.choice(quotes)}")
    st.markdown(f"**📘 Book Pick:** {random.choice(books)}")
    st.markdown(f"<i>{random.choice(poems)}</i>", unsafe_allow_html=True)
    st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 0.8em; color: gray;'>
    📚 Data from <a href='https://openlibrary.org/developers/api' target='_blank'>Open Library</a> |
    💬 AI via <a href='https://openrouter.ai/' target='_blank'>OpenRouter</a> |
    🎨 Built with ❤️ using Streamlit  
    <br>
    © 2025 Varsha T. All rights reserved.
</div>
""", unsafe_allow_html=True)

