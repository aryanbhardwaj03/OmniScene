from abc import ABC, abstractmethod
import numpy as np
from typing import Any, Dict

class BaseModel(ABC):
    """Abstract base class for all OmniScene ML models."""
    
    def __init__(self, version: str):
        self.version = version
        self.is_loaded = False
        self.model = None

    @abstractmethod
    def load(self) -> None:
        """Load model weights and prepare for inference."""
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload model to free memory."""
        pass

    @abstractmethod
    async def predict(self, image: Any) -> Dict[str, Any]:
        """Run inference on the provided image."""
        pass

class BaseClassifier(BaseModel):
    """Base for classification models."""
    pass

class BaseDetector(BaseModel):
    """Base for object detection models."""
    pass

class BaseEmbeddingModel(BaseModel):
    """Base for embedding generators."""
    pass
