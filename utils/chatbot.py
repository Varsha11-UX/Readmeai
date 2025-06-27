import streamlit as st
import httpx

def ask_reading_buddy(question):
    api_key = st.secrets.get("OPENROUTER_API_KEY")

    # 🛑 Check if API key is missing
    if not api_key:
        return "🚫 API key not found. Please contact the developer."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful AI book companion. Recommend books, summarize, answer queries."},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "❌ Unauthorized. Check if your OpenRouter API key is valid."
        return f"❌ Chatbot error: {e.response.status_code} - {e.response.text}"

    except Exception as e:
        return f"⚠️ Something went wrong: {str(e)}"
