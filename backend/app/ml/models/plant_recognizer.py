import torch
from PIL import Image
import io
from app.ml.base import BaseClassifier
from app.ml.registry import model_registry
import logging

logger = logging.getLogger(__name__)

class PlantRecognizer(BaseClassifier):
    """Recognizes plant species using zero-shot CLIP classification."""
    
    def __init__(self):
        super().__init__(version="clip-plant-recognizer-v1")
        # List of common indoor/outdoor plants and crops
        self.plants = [
            "snake plant", "monstera", "golden pothos", "spider plant", 
            "aloe vera", "peace lily", "rubber plant", "fiddle leaf fig",
            "zz plant", "jade plant", "philodendron", "cast iron plant",
            "tomato", "potato", "bell pepper", "corn", "apple", "grape",
            "cherry", "peach", "strawberry", "squash", "orange", "lemon",
            "rose", "tulip", "sunflower", "orchid", "fern", "cactus", "succulent",
            "bamboo", "bonsai", "ivy", "basil", "mint", "rosemary", "thyme"
        ]
        self.prompts = [f"a photo of a {p} plant" for p in self.plants]
        
    def load(self) -> None:
        # We reuse the CLIP model from the scene classifier to save memory!
        self.scene_model = model_registry.get_model("scene_classifier")
        if not self.scene_model.is_loaded:
            self.scene_model.load()
        self.is_loaded = True
        
    def unload(self) -> None:
        self.is_loaded = False
        
    async def predict(self, image_bytes: bytes) -> dict:
        if not self.is_loaded:
            self.load()
            
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            
            inputs = self.scene_model.processor(
                text=self.prompts, 
                images=image, 
                return_tensors="pt", 
                padding=True
            ).to(self.scene_model.device)
            
            with torch.no_grad():
                outputs = self.scene_model.model(**inputs)
                
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]
            
            max_idx = probs.argmax()
            species_name = self.plants[max_idx].title()
            confidence = float(probs[max_idx])
            
            # Determine confidence level
            if confidence >= 0.85:
                level = "HIGH"
            elif confidence >= 0.50:
                level = "MEDIUM"
            else:
                level = "LOW"
                
            return {
                "common_name": species_name,
                "scientific_name": species_name + " (Species)",
                "confidence": confidence,
                "confidence_level": level
            }
        except Exception as e:
            logger.error(f"Error in PlantRecognizer: {e}")
            raise e
