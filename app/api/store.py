from fastapi import APIRouter, HTTPException, Depends
from pathlib import Path
import shutil
from app.models.schemas import StoreRequest
from app.utils.validators import safe_path_join
from app.utils.auth import verify_token
from app.core.config import BASE_PATH, TEMPLATE_PATH

router = APIRouter(prefix="/store", tags=["store"])

@router.post("")
async def create_store(request: StoreRequest, token: str = Depends(verify_token)):
    """Create store directory structure and copy template files"""
    store_path = safe_path_join(BASE_PATH, request.storeid)
    json_path = store_path / "json"
    image_path = store_path / "image"
    
    if store_path.exists():
        raise HTTPException(status_code=409, detail="Store already exists")
    
    try:
        json_path.mkdir(parents=True, exist_ok=True)
        image_path.mkdir(parents=True, exist_ok=True)
        
        template_path = Path(TEMPLATE_PATH)
        if template_path.exists():
            for file_path in template_path.glob("*.json"):
                shutil.copy2(file_path, json_path)
        
        return {"message": f"Store {request.storeid} created"}
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to create store")