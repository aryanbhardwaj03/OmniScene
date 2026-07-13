import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import io
import logging
from app.ml.base import BaseClassifier

logger = logging.getLogger(__name__)

class AnimalRecognizer(BaseClassifier):
    """
    Recognizes dog breeds (and potentially other animals in the future).
    For V1, uses a ViT model fine-tuned on 120 dog breeds.
    """
    def __init__(self):
        super().__init__(version="dog-breed-vit-v1")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = "wesleyacheng/dog-breeds-multiclass-image-classification-with-vit"
        
    def load(self) -> None:
        if self.is_loaded:
            return
        logger.info(f"Loading Animal Recognizer model ({self.model_id}) on {self.device}...")
        try:
            self.processor = AutoImageProcessor.from_pretrained(self.model_id)
            self.model = AutoModelForImageClassification.from_pretrained(self.model_id).to(self.device)
            self.model.eval()
            self.is_loaded = True
        except Exception as e:
            logger.error(f"Failed to load Animal Recognizer model: {e}")
            self.is_loaded = False

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
                
            logits = outputs.logits
            probs = logits.softmax(dim=1).cpu().numpy()[0]
            max_idx = probs.argmax()
            predicted_class = self.model.config.id2label[max_idx]
            confidence = float(probs[max_idx])
            
            # Clean up class name (e.g., "golden_retriever" to "Golden Retriever")
            breed_name = predicted_class.replace("_", " ").title()
            
            # Determine confidence level
            if confidence >= 0.85:
                level = "HIGH"
            elif confidence >= 0.60:
                level = "MEDIUM"
            else:
                level = "LOW"
                
            return {
                "common_name": breed_name,
                "scientific_name": "Canis lupus familiaris",
                "confidence": confidence,
                "confidence_level": level,
                "target_layer": None # No Grad-CAM for ViT yet
            }
        except Exception as e:
            logger.error(f"Error in Animal Recognizer prediction: {e}")
            raise e
