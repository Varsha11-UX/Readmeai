import streamlit as st
import httpx

def ask_reading_buddy(question):
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "google/gemini-2.5-pro",  # 🔄 Updated model name
            "messages": [
                {"role": "system", "content": "You are a helpful AI book companion. Recommend books, summarize, answer queries."},
                {"role": "user", "content": question}
            ]
        }
        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Chatbot error: {str(e)}"
