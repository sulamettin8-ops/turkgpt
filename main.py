import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# Groq API Key
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Sohbet geçmişi (sistem talimatı dahil)
chat_history = [
    {
        "role": "system",
        "content": "Sen TurkGPT adında samimi, zeki, espri anlayışı olan ve Türkçe konuşan harika bir yapay zeka arkadaşısın."
    }
]


class MessageRequest(BaseModel):
    message: str


@app.post("/api/chat")
async def chat_endpoint(req: MessageRequest):
    user_msg = req.message
    chat_history.append({"role": "user", "content": user_msg})

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=chat_history,
            temperature=0.7,
        )
        bot_response = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_response})
        return {"response": bot_response}
    except Exception as e:
        return {"response": f"Bir hata oluştu: {str(e)}"}


@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()
