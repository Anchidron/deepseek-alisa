import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

DEEPSEEK_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Список бесплатных моделей — если одна перегружена, пробуем следующую
MODELS = [
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "tencent/hy3-preview:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-nemo:free",
]

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]

    answer = None
    for model in MODELS:
        try:
            response = requests.post(
                DEEPSEEK_API_URL,
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "Отвечай кратко, не более 2-3 предложений."},
                        {"role": "user", "content": user_text}
                    ],
                    "max_tokens": 200
                },
                timeout=4
            )

            print(f"MODEL {model} STATUS:", response.status_code)

            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                break  # Успех — выходим из цикла

        except Exception as e:
            print(f"MODEL {model} ERROR:", e)

    if not answer:
        answer = "Извините, все модели сейчас перегружены. Попробуйте через минуту."

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
