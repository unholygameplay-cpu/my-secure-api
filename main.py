from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Priyanshu Secure AI API", version="2.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 AAPKI PERSONAL SECRET API KEY
# Is password ko sirf tum jante ho aur tumhari website janti hai!
PRIYANSHU_SECRET_KEY = "PriyanshuSecretVIP99"

# Security Verification Function
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key is None or x_api_key != PRIYANSHU_SECRET_KEY:
        # Agar key galat hui ya nahi bheji, toh direct block!
        raise HTTPException(status_code=403, detail="Unauthorized Access! Priyanshu Server is Locked.")
    return x_api_key

class ChatPrompt(BaseModel):
    prompt: str

# 🚀 Secure Endpoint (Ab ye Depends(verify_api_key) se protected hai)
@app.post("/v1/chat")
async def generate_response(data: ChatPrompt, api_key: str = Depends(verify_api_key)):
    
    custom_reply = f"Priyanshu API Node Secure! Aapka sawaal '{data.prompt}' successfully process ho gaya. Backend Engine ekdum makkhan chal raha hai bhai!"
    
    return {
        "status": "success",
        "author": "Priyanshu Mishra",
        "choices": [{
            "message": {
                "role": "assistant",
                "content": custom_reply
            }
        }]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
