from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import logging

from app.core.database import get_db
from app.models.analysis import AnalysisResultDB
from app.schemas.analysis import AnalysisResponse
from app.models.user import UserDB
from app.api.deps import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/history")
async def get_history(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Get paginated analysis history."""
    try:
        offset = (page - 1) * size
        
        # In a real app we'd get total count, but simplifying for V1
        stmt = select(AnalysisResultDB).filter(AnalysisResultDB.user_id == current_user.id).order_by(desc(AnalysisResultDB.timestamp)).offset(offset).limit(size)
        result = await db.execute(stmt)
        items = result.scalars().all()
        
        # For full AnalysisResponse matching, we'd reconstruct. 
        # Here we just return the raw DB dicts as a list for simplicity.
        history = []
        for item in items:
            history.append({
                "id": item.id,
                "timestamp": item.timestamp,
                "scene_category": item.scene_category,
                "scene_confidence": item.scene_confidence,
                "detections": item.detections,
                "processing_time_ms": item.processing_time_ms
            })
            
        return {
            "items": history,
            "page": page,
            "size": size,
            "total": -1 # Total count omitted for brevity
        }
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail="Error fetching history")
