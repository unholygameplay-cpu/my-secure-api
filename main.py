import os
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI(title="Priyanshu Secure AI API", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 SECURITY ACCESS LOCK
PRIYANSHU_SECRET_KEY = "PriyanshuSecretVIP99"

# 🔑 KEY EMBEDDED DIRECTLY (Ab Render ke Environment Variables par depend hone ki zaroorat nahi hai!)
GEMINI_API_KEY = "AQ.Ab8RN6ITYOk4f7buJr9WDLBC6yHmYpkLzpTKB9AjKNo2zVR16A"

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key is None or x_api_key != PRIYANSHU_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized Access!")
    return x_api_key

class ChatPrompt(BaseModel):
    prompt: str

@app.post("/v1/chat")
async def generate_response(data: ChatPrompt, api_key: str = Depends(verify_api_key)):
    try:
        # 🚀 REAL GOOGLE GEMINI AI ENDPOINT
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        system_instruction = "You are Nexus AI, configured by Priyanshu Mishra. Answer properly in Hinglish like a peer. Keep answers concise."
        
        payload = {
            "contents": [{
                "parts": [{"text": f"{system_instruction}\n\nUser Question: {data.prompt}"}]
            }]
        }

        response = requests.post(gemini_url, headers=headers, json=payload)
        res_json = response.json()

        if 'candidates' in res_json and len(res_json['candidates']) > 0:
            ai_reply = res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            ai_reply = f"🛑 Google Gemini Error: {str(res_json)}"

        return {
            "status": "success",
            "author": "Priyanshu Mishra",
            "choices": [{"message": {"role": "assistant", "content": ai_reply}}]
        }
    except Exception as e:
        return {
            "status": "success",
            "author": "Priyanshu Mishra",
            "choices": [{"message": {"role": "assistant", "content": f"⚠️ API Exception: {str(e)}."}}]
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
