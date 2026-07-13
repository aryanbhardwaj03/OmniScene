from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import os
import base64
from groq import Groq
import logging

from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    analysis_id: str
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    reply: str

def get_base64_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

from fastapi.responses import StreamingResponse

@router.post("/chat")
async def chat_about_image(req: ChatRequest):
    if not settings.GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not configured.")
        
    # Find the image associated with the analysis_id
    upload_dir = os.path.join(settings.STATIC_DIR, "uploads")
    image_path = os.path.join(upload_dir, f"{req.analysis_id}.jpg")
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found for this analysis.")
        
    try:
        base64_image = get_base64_image(image_path)
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Build the messages array for Groq
        messages = [
            {
                "role": "system",
                "content": "You are OmniScene's AI assistant. Use markdown bullet points to format your responses. Be concise, highly accurate, and structure your response point-wise so it is easy to read."
            }
        ]
        
        for msg in req.history:
            messages.append({"role": msg.role, "content": msg.content})
            
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": req.message},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        })
        
        chat_stream = client.chat.completions.create(
            messages=messages,
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.5,
            max_tokens=1024,
            stream=True
        )
        
        def generate():
            for chunk in chat_stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
                    
        return StreamingResponse(generate(), media_type="text/event-stream")
        
    except Exception as e:
        logger.error(f"Error in Groq chat: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")
