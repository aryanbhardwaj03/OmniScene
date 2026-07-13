from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from .common import ImageMeta
from .detection import DetectionResult

class SimilarImage(BaseModel):
    id: str
    similarity: float
    thumbnail_url: str

class AnalysisRequest(BaseModel):
    pass  # Usually handled via form-data for file uploads

class AnalysisResponse(BaseModel):
    id: str
    timestamp: datetime
    image_size: ImageMeta
    scene_category: str
    scene_confidence: float
    detections: List[DetectionResult]
    similar_images: List[SimilarImage]
    processing_time_ms: int
    model_versions: Dict[str, str]
