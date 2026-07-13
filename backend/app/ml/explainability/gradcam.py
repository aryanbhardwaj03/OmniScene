import io
import os
import uuid
import numpy as np
import torch
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget

from app.ml.models.plant_village import shared_plant_model
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class ExplainabilityEngine:
    """Generates Grad-CAM visual explanations."""
    
    def __init__(self):
        # target_layers needs to be a list
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    async def generate_explanation(self, image_bytes: bytes, target_class_idx: int = None) -> dict:
        """
        Generates GradCAM for the image. If target_class_idx is None,
        it uses the highest scoring class.
        Returns a relative URL to the saved heatmap image.
        """
        if not shared_plant_model.is_loaded:
            shared_plant_model.load()
            
        model = shared_plant_model.model
        processor = shared_plant_model.processor
        
        try:
            # Prepare image
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            
            # For the visualization, we need an RGB image normalized to [0,1]
            # Resize it to match the model input size (usually 224x224)
            vis_img = pil_img.resize((224, 224))
            rgb_img = np.float32(vis_img) / 255.0

            inputs = processor(images=pil_img, return_tensors="pt").to(self.device)
            input_tensor = inputs["pixel_values"]
            
            # Target the last layer of the MobileNetV2 features
            # The model is AutoModelForImageClassification over MobileNetV2
            target_layers = [model.mobilenet_v2.conv_1x1]
            
            # Construct the CAM object once, and then re-use it on many images:
            
            # HuggingFace models return an object, but GradCAM expects a raw tensor
            class HFWrapper(torch.nn.Module):
                def __init__(self, m):
                    super().__init__()
                    self.m = m
                def forward(self, x):
                    return self.m(x).logits
                    
            wrapped_model = HFWrapper(model)
            
            with GradCAM(model=wrapped_model, target_layers=target_layers) as cam:
                
                targets = None
                if target_class_idx is not None:
                    targets = [ClassifierOutputTarget(target_class_idx)]
                    
                # You can also pass aug_smooth=True and eigen_smooth=True, to apply smoothing.
                grayscale_cam = cam(input_tensor=input_tensor, targets=targets)
                
                # In this example grayscale_cam has only one image in the batch:
                grayscale_cam = grayscale_cam[0, :]
                
                visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
                
            # Save the visualization
            heatmap_id = str(uuid.uuid4())
            filename = f"{heatmap_id}.png"
            filepath = os.path.join(settings.STATIC_DIR, filename)
            
            Image.fromarray(visualization).save(filepath)
            
            # Simple heuristic for top regions based on high-activation pixels
            # In a real app we might map coordinates back to meaningful terms
            top_regions = ["Highly activated disease symptoms area"]
            
            return {
                "gradcam_url": f"/static/{filename}",
                "top_regions": top_regions
            }
            
        except Exception as e:
            logger.error(f"Error generating Grad-CAM: {e}")
            return {
                "gradcam_url": None,
                "top_regions": []
            }

explainability_engine = ExplainabilityEngine()
