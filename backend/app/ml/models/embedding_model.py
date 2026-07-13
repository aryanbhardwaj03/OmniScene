import torch
import torch.nn.functional as F
from PIL import Image
from transformers import AutoImageProcessor, AutoModel
import io
import numpy as np
import logging

from app.ml.base import BaseEmbeddingModel

logger = logging.getLogger(__name__)

class Dinov2EmbeddingModel(BaseEmbeddingModel):
    """Generates visual embeddings using DINOv2."""
    
    def __init__(self):
        super().__init__(version="dinov2-base-v1")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = "facebook/dinov2-base"
        
    def load(self) -> None:
        if self.is_loaded:
            return
        logger.info(f"Loading DINOv2 ({self.model_id}) on {self.device}...")
        self.processor = AutoImageProcessor.from_pretrained(self.model_id)
        self.model = AutoModel.from_pretrained(self.model_id).to(self.device)
        self.model.eval()
        self.is_loaded = True

    def unload(self) -> None:
        if self.is_loaded:
            del self.model
            del self.processor
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            self.is_loaded = False

    async def predict(self, image_bytes: bytes) -> dict:
        if not self.is_loaded:
            self.load()
            
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            # Use the CLS token embedding (first token)
            embeddings = outputs.last_hidden_state[:, 0, :]
            
            # L2 Normalize for cosine similarity in FAISS
            embeddings = F.normalize(embeddings, p=2, dim=1)
            
            embedding_np = embeddings.cpu().numpy()[0]
            
            return {
                "embedding": embedding_np,
                "dimension": embedding_np.shape[0]
            }
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise e
