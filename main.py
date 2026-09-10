import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai
from google.genai import types

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Google AI Studio'dan aldığın AIzaSy... ile başlayan anahtarın
API_KEY = "AIzaSyAA89xd7aVM938cKhmbDWIMMyiNqAzDUlg"

# Yeni resmi Gemini istemcisi (client)
client = genai.Client(api_key=API_KEY)

SYSTEM_INSTRUCTION = (
    "Sen TurkGPT adında gelişmiş bir Türkçe yapay zeka asistanısın. "
    "Seni geliştiren kişiler R. Aybars ve OpenAI'dır. "
    "Kullanıcılara saygılı, yardımsever ve Türkçe dil kurallarına uygun yanıtlar verirsin."
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        
        if not user_message:
            return {"response": "Lütfen bir mesaj yazın."}

        # Güncel Gemini Flash modeli kullanımı
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
            ),
        )

        reply = response.text if response.text else "Yanıt oluşturulamadı."
        return {"response": reply}

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return {"response": f"Üzgünüm, bir hata oluştu: {str(e)}"}
