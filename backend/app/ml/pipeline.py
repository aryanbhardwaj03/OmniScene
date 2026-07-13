import uuid
import time
from datetime import datetime
import logging
from PIL import Image
import io
import base64
import json
import os
from groq import Groq

from app.ml.registry import model_registry
from app.ml.models.embedding_model import Dinov2EmbeddingModel
from app.ml.vector_store.faiss_store import faiss_store
from app.schemas.analysis import AnalysisResponse, SimilarImage
from app.schemas.detection import DetectionResult, SpeciesInfo, DiseaseInfo
from app.schemas.common import ImageMeta
from app.config import settings

logger = logging.getLogger(__name__)

# Register models (only embedding model remains local)
model_registry.register_class("embedding_model", Dinov2EmbeddingModel)

def get_base64_from_bytes(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode('utf-8')

async def analyze_image_pipeline(image_bytes: bytes) -> dict:
    """Full inference pipeline orchestrator using Groq VLM."""
    start_time = time.time()
    analysis_id = str(uuid.uuid4())
    
    # 1. Metadata
    img = Image.open(io.BytesIO(image_bytes))
    image_size = ImageMeta(width=img.width, height=img.height, format=img.format or "JPEG")
    
    # Save the image so Groq and Similar Cases can reference it locally later if needed
    upload_dir = os.path.join(settings.STATIC_DIR, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    image_path = os.path.join(upload_dir, f"{analysis_id}.jpg")
    img.convert("RGB").save(image_path, "JPEG")
    
    # 2. VLM Analysis with Groq
    base64_image = get_base64_from_bytes(image_bytes)
    client = Groq(api_key=settings.GROQ_API_KEY)
    
    system_prompt = """
    You are an expert biological and general image analysis AI. 
    Analyze the provided image and output a raw JSON object with NO markdown formatting, NO backticks, and NO intro/outro text.
    The JSON must strictly follow this structure:
    {
      "scene_category": "plant" | "animal" | "human" | "other",
      "species": {
        "common_name": "String (e.g., Golden Retriever, Snake Plant)",
        "scientific_name": "String (e.g., Canis lupus familiaris, Sansevieria trifasciata) or N/A",
        "confidence": 0.95,
        "confidence_level": "HIGH" | "MEDIUM" | "LOW"
      },
      "disease": {
        "name": "String (e.g., Healthy, Leaf Blight, Fleas) or 'Healthy' if none",
        "confidence": 0.90,
        "confidence_level": "HIGH" | "MEDIUM" | "LOW",
        "symptoms": ["List of symptom strings"],
        "management": ["List of management advice strings"]
      }
    }
    Make sure to give an accurate description based on the image. If it's a human, just say "Human" for species. If it's a plant or animal, give the specific species or breed. If healthy, state "Healthy".
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this image and return the JSON object."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.1,
            max_tokens=1024,
        )
        
        raw_reply = chat_completion.choices[0].message.content.strip()
        # Clean up any potential markdown if Groq disobeys
        if raw_reply.startswith("```json"):
            raw_reply = raw_reply[7:-3]
        elif raw_reply.startswith("```"):
            raw_reply = raw_reply[3:-3]
            
        ai_data = json.loads(raw_reply)
        category = ai_data.get("scene_category", "other")
        
    except Exception as e:
        logger.error(f"Groq API Error: {e}")
        # Fallback if Groq fails or rate limits
        category = "other"
        ai_data = {
            "scene_category": "other",
            "species": {"common_name": "Unknown", "scientific_name": "N/A", "confidence": 1.0, "confidence_level": "UNKNOWN"},
            "disease": {"name": "Analysis Failed", "confidence": 1.0, "confidence_level": "UNKNOWN", "symptoms": [], "management": []}
        }
        
    detections = [
        DetectionResult(
            category=category,
            species=SpeciesInfo(**ai_data["species"]),
            disease=DiseaseInfo(**ai_data["disease"])
        )
    ]
        
    # 3. Generate Embeddings and Search (Local DINOv2)
    embed_model = model_registry.get_model("embedding_model")
    embed_res = await embed_model.predict(image_bytes)
    embedding = embed_res["embedding"]
    
    # Search similar BEFORE adding this new one
    similar_raw = faiss_store.search(embedding, k=5)
    similar_images = []
    for s in similar_raw:
        similar_images.append(SimilarImage(
            id=s["id"],
            similarity=s["similarity"],
            thumbnail_url=s["metadata"].get("thumbnail_url", "")
        ))
        
    # Add new embedding to store
    meta = {
        "category": category,
        "thumbnail_url": f"/static/uploads/{analysis_id}.jpg"
    }
    faiss_store.add_embedding(analysis_id, embedding, meta)
    
    processing_time = int((time.time() - start_time) * 1000)
    
    return {
        "id": analysis_id,
        "timestamp": datetime.utcnow(),
        "image_size": image_size.model_dump(),
        "scene_category": category,
        "scene_confidence": 1.0,  # Groq doesn't provide a top-level scene confidence
        "detections": [d.model_dump() for d in detections],
        "similar_images": [s.model_dump() for s in similar_images],
        "processing_time_ms": processing_time,
        "model_versions": {"vision_llm": "llama-4-scout", "embedding": "dinov2_vits14"}
    }

