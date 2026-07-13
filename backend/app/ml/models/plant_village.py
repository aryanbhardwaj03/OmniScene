import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import io
import logging
from app.ml.base import BaseClassifier
from app.config import settings
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PlantVillageUnifiedModel(BaseClassifier):
    """
    A unified model for PlantVillage that handles both species and disease.
    We load it once and use it for both PlantRecognizer and DiseaseDetector
    to save memory in V1.
    """
    def __init__(self):
        super().__init__(version="plantvillage-resnet-v1")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
        
    def load(self) -> None:
        if self.is_loaded:
            return
        logger.info(f"Loading PlantVillage model ({self.model_id}) on {self.device}...")
        try:
            # The fine-tuned model's repo is missing image processor config
            # so we use the base MobileNetV2 processor which has the same requirements
            self.processor = AutoImageProcessor.from_pretrained("google/mobilenet_v2_1.0_224")
            self.model = AutoModelForImageClassification.from_pretrained(self.model_id).to(self.device)
            self.model.eval()
            self.is_loaded = True
        except Exception as e:
            logger.error(f"Failed to load PlantVillage model: {e}")
            self.is_loaded = False

    def unload(self) -> None:
        if self.is_loaded:
            del self.model
            del self.processor
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            self.is_loaded = False

    async def predict(self, image_bytes: bytes) -> Dict[str, Any]:
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
            
            # PlantVillage classes format: "Species___Disease_name"
            parts = predicted_class.split("___")
            species_raw = parts[0] if len(parts) > 0 else "Unknown"
            disease_raw = parts[1] if len(parts) > 1 else "Unknown"
            
            # Clean up names
            species = species_raw.replace("_", " ")
            disease = disease_raw.replace("_", " ")
            
            return {
                "species": species,
                "disease": disease,
                "confidence": confidence,
                "raw_class": predicted_class,
                "target_layer": self.model.classifier if hasattr(self.model, "classifier") else None 
            }
        except Exception as e:
            logger.error(f"Error in PlantVillage prediction: {e}")
            raise e

# Singleton instance to share between recognizer and detector
shared_plant_model = PlantVillageUnifiedModel()
