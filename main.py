import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

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
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Отвечай кратко, не более 2-3 предложений."},
                    {"role": "user", "content": user_text}
                ],
                "max_tokens": 200
            },
            timeout=4
        )

        print("DEEPSEEK STATUS:", response.status_code)
        print("DEEPSEEK BODY:", response.text)

        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
        else:
            answer = "Извините, сервис временно недоступен. Попробуйте позже."

    except Exception as e:
        print("ERROR:", e)
        answer = "Извините, я не успел подумать. Попробуйте спросить покороче."

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
