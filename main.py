import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Адрес API OpenRouter
DEEPSEEK_API_URL = "https://openrouter.ai/api/v1/chat/completions"
# Ключ берём из переменной окружения OPENROUTER_API_KEY
DEEPSEEK_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]

    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/free",
                "messages": [{"role": "user", "content": user_text}],
                "max_tokens": 300  # Ограничиваем длину ответа для скорости
            },
            timeout=4  # Ждём не больше 4 секунд, чтобы уложиться в лимит Алисы
        )

        print("OPENROUTER STATUS:", response.status_code)
        print("OPENROUTER BODY:", response.text)

        answer = response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("ERROR:", e)
        answer = "Извините, я не успел подумать. Попробуйте спросить что-нибудь покороче."

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
