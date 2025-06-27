import streamlit as st
from utils.recommender import get_books_by_genre
from utils.chatbot import ask_reading_buddy

st.set_page_config(page_title="ReadWise AI", page_icon="📚", layout="wide")

# Optional: Background (comment if causing issues)
# def set_background():
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("https://images.unsplash.com/photo-1535909339361-5877921a7d4b");
#             background-size: cover;
#             background-position: center;
#             background-repeat: no-repeat;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
# set_background()

# Title banner
st.markdown("""
<div style="background: linear-gradient(90deg, #ff914d, #ffcd8c); padding: 2rem; border-radius: 15px; text-align: center; color: white;">
    <h1>📚 ReadWise AI</h1>
    <p>Discover books that match your mood. Ask anything. Buy smarter.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Recommendations", "🤖 Chatbot", "🛍️ Buy Smart"])

with tab1:
    st.subheader("📖 Mood/Genre-Based Book Recommendations")
    query = st.text_input("Enter your mood or favorite genre (e.g., happy, sci-fi, historical):")

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

with tab2:
    st.subheader("🤖 Ask Your Reading Buddy")
    user_input = st.text_area("💬 Ask something about books, quotes, genres...")

    if st.button("🎙️ Ask Chatbot"):
        if user_input:
            with st.spinner("Thinking..."):
                reply = ask_reading_buddy(user_input)
            st.success(reply)
        else:
            st.warning("Please enter a message.")

with tab3:
    st.subheader("🛍️ Buy a Book Online")
    title = st.text_input("Search a book to buy (e.g., Atomic Habits):")
    if title:
        q = title.replace(" ", "+")
        st.markdown(f"- 🛍️ [Amazon](https://www.amazon.in/s?k={q})")
        st.markdown(f"- 🛒 [Flipkart](https://www.flipkart.com/search?q={q})")

# 🎁 Surprise Me
import random
st.markdown("---")
st.markdown("<h2 style='text-align:center;'>🎁 Surprise Me!</h2>", unsafe_allow_html=True)

if st.button("✨ Click for a Surprise!", key="surprise"):
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
