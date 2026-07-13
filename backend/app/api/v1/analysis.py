from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import os
from app.ml.pipeline import analyze_image_pipeline
from app.schemas.analysis import AnalysisResponse
from app.config import settings
from app.core.database import get_db
from app.models.analysis import AnalysisResultDB
from app.models.user import UserDB
from app.api.deps import get_current_user_optional

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image_endpoint(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user_optional)
):
    """Analyze an uploaded image using the OmniScene AI pipeline."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
        
    try:
        # Read the file into memory
        contents = await file.read()
        
        # Run inference pipeline
        result = await analyze_image_pipeline(contents)
        
        # Save to database
        db_result = AnalysisResultDB(
            id=result["id"],
            image_width=result["image_size"]["width"],
            image_height=result["image_size"]["height"],
            image_format=result["image_size"]["format"],
            scene_category=result["scene_category"],
            scene_confidence=result["scene_confidence"],
            processing_time_ms=result["processing_time_ms"],
            detections=result["detections"],
            model_versions=result["model_versions"],
            user_id=current_user.id if current_user else None
        )
        db.add(db_result)
        await db.commit()
        
        # Save original image for reference / history / similarity search thumbs
        upload_dir = os.path.join(settings.STATIC_DIR, "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        # In real app we'd convert/compress to jpg thumbnail
        file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        saved_path = os.path.join(upload_dir, f"{result['id']}.{file_ext}")
        with open(saved_path, "wb") as f:
            f.write(contents)
            
        # Update thumbnail_url in the result (and ideally in FAISS meta, though pipeline just did it)
        result["similar_images"] = result["similar_images"] # remains same
        
        return result
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")
