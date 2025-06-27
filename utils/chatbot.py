import streamlit as st
import httpx

def ask_reading_buddy(question):
    api_key = st.secrets["OPENROUTER_API_KEY"]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful reading assistant."},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=20
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except httpx.HTTPStatusError as e:
        return f"❌ Chatbot error: {e.response.status_code} - {e.response.text}"
