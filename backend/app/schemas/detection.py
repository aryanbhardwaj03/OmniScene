from pydantic import BaseModel
from typing import Optional, List
from .common import ConfidenceLevel

class SpeciesInfo(BaseModel):
    common_name: str
    scientific_name: str
    confidence: float
    confidence_level: ConfidenceLevel

class DiseaseInfo(BaseModel):
    name: str
    scientific_name: Optional[str] = None
    confidence: float
    confidence_level: ConfidenceLevel
    severity: Optional[str] = None
    symptoms: List[str] = []
    management: List[str] = []

class ExplainabilityInfo(BaseModel):
    gradcam_url: Optional[str] = None
    top_regions: List[str] = []

class BoundingBox(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float

class DetectionResult(BaseModel):
    category: str  # plant, animal, insect, human, etc.
    species: Optional[SpeciesInfo] = None
    disease: Optional[DiseaseInfo] = None
    explainability: Optional[ExplainabilityInfo] = None
    bounding_box: Optional[BoundingBox] = None
