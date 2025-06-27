import os
import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

def ask_reading_buddy(prompt):
    if not api_key:
        return "API key missing. Please set OPENROUTER_API_KEY in your .env file."

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "ReadWise AI",
        }

        payload = {
            "model": "gpt-4o-mini",  # ✅ Correct field and supported model
            "messages": [{"role": "user", "content": prompt}],
        }

        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ Chatbot error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Chatbot exception: {str(e)}"
