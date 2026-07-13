from typing import Dict, Optional, Type
import logging
from app.ml.base import BaseModel

logger = logging.getLogger(__name__)

class ModelRegistry:
    """Singleton registry to manage ML models lifecycle."""
    
    def __init__(self):
        self._models: Dict[str, BaseModel] = {}
        self._classes: Dict[str, Type[BaseModel]] = {}
    
    def register_class(self, name: str, model_class: Type[BaseModel]):
        self._classes[name] = model_class
        
    def get_model(self, name: str) -> BaseModel:
        """Get a loaded model by name. Loads it if not already loaded."""
        if name not in self._models:
            if name not in self._classes:
                raise ValueError(f"Model class {name} is not registered.")
            
            logger.info(f"Instantiating and loading model: {name}")
            model_instance = self._classes[name]()
            model_instance.load()
            self._models[name] = model_instance
            
        return self._models[name]
    
    async def load_all(self):
        """Pre-load all registered models."""
        for name in self._classes.keys():
            self.get_model(name)
            
    async def unload_all(self):
        """Unload all models to free memory."""
        for name, model in self._models.items():
            model.unload()
        self._models.clear()

    def get_versions(self) -> Dict[str, str]:
        """Return versions of all currently loaded models."""
        return {name: model.version for name, model in self._models.items()}

# Global singleton
model_registry = ModelRegistry()
