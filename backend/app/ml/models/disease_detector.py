from app.ml.base import BaseDetector
from app.ml.models.plant_village import shared_plant_model
import logging

logger = logging.getLogger(__name__)

class DiseaseDetector(BaseDetector):
    """Detects plant diseases using the shared PlantVillage model."""
    
    def __init__(self):
        super().__init__(version="plantvillage-disease-v1")
        self.shared_model = shared_plant_model
        
    def load(self) -> None:
        self.shared_model.load()
        self.is_loaded = True
        
    def unload(self) -> None:
        self.is_loaded = False
        
    async def predict(self, image_bytes: bytes) -> dict:
        result = await self.shared_model.predict(image_bytes)
        
        conf = result["confidence"]
        disease = result["disease"]
        
        if conf >= 0.85:
            level = "HIGH"
        elif conf >= 0.60:
            level = "MEDIUM"
        else:
            level = "LOW"
            
        # Basic mocked info based on disease
        symptoms = ["Visual abnormalities on leaves"]
        management = ["Remove affected leaves", "Apply appropriate fungicide if fungal"]
        severity = "moderate"
        
        if disease.lower() == "healthy":
            symptoms = ["None"]
            management = ["Maintain current care"]
            severity = "none"
            
        return {
            "name": disease,
            "confidence": conf,
            "confidence_level": level,
            "severity": severity,
            "symptoms": symptoms,
            "management": management,
            "raw_class": result["raw_class"],
            "target_layer": result["target_layer"]
        }
