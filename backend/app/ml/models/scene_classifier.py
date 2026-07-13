import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from app.ml.base import BaseClassifier
from app.config import settings
import io
import logging

logger = logging.getLogger(__name__)

class SceneClassifier(BaseClassifier):
    """Uses CLIP to classify the general scene category."""
    
    def __init__(self):
        super().__init__(version="clip-vit-base-patch32-v1")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = "openai/clip-vit-base-patch32"
        self.categories = ["plant", "animal", "insect", "human face", "landscape", "other"]
        # Create prompts for CLIP
        self.prompts = [f"a photo of a {c}" for c in self.categories]

    def load(self) -> None:
        if self.is_loaded:
            return
        logger.info(f"Loading SceneClassifier ({self.model_id}) on {self.device}...")
        self.processor = CLIPProcessor.from_pretrained(self.model_id)
        self.model = CLIPModel.from_pretrained(self.model_id).to(self.device)
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
            
            inputs = self.processor(
                text=self.prompts, 
                images=image, 
                return_tensors="pt", 
                padding=True
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]
            
            max_idx = probs.argmax()
            category = self.categories[max_idx]
            confidence = float(probs[max_idx])
            
            # Map 'human face' to 'human' for internal consistency
            if category == "human face":
                category = "human"
                
            # Use confidence thresholds
            if confidence < settings.CONFIDENCE_LOW:
                category = "unknown"
                
            return {
                "category": category,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"Error in SceneClassifier: {e}")
            raise e
