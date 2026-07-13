from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"

class ImageMeta(BaseModel):
    width: int
    height: int
    format: str

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
