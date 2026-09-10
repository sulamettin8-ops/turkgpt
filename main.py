import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import google.generativeai as genai

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Gemini API Yapılandırması
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6LOWEVjTvn7HMrxIUotSVDCz5iWzqNo-xL9IOCPQiYlDA")
genai.configure(api_key=GEMINI_API_KEY)

# Sistem Talimatı ve Model Ayarları
SYSTEM_INSTRUCTION = (
    "Sen TurkGPT adında gelişmiş bir Türkçe yapay zeka asistanısın. "
    "Seni geliştiren kişiler R. Aybars ve OpenAI'dır. "
    "Kullanıcılara saygılı, yardımsever ve Türkçe dil kurallarına uygun yanıtlar verirsin."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
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

        response = model.generate_content(user_message)
        reply = response.text if response.text else "Yanıt oluşturulamadı."
        return {"response": reply}

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return {"response": f"Üzgünüm, bir hata oluştu: {str(e)}"}
