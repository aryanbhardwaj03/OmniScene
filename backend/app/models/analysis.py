import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class AnalysisResultDB(Base):
    __tablename__ = "analysis_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    image_width = Column(Integer)
    image_height = Column(Integer)
    image_format = Column(String)
    
    scene_category = Column(String)
    scene_confidence = Column(Float)
    processing_time_ms = Column(Integer)
    
    # We store detections as JSON for simplicity in V1
    detections = Column(JSON, default=list)
    model_versions = Column(JSON, default=dict)
    
    # Optional user association
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    user = relationship("UserDB", backref="analyses")
