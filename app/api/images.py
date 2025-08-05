from fastapi import APIRouter, HTTPException, Depends
from app.utils.validators import safe_path_join
from app.utils.auth import verify_token
from app.core.config import BASE_PATH

router = APIRouter(prefix="/images", tags=["images"])

@router.get("/{storeid}")
async def list_images(storeid: str, token: str = Depends(verify_token)):
    """List all images in store"""
    image_path = safe_path_join(BASE_PATH, storeid, "image")
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    try:
        files = [f.name for f in image_path.iterdir() if f.is_file()]
        image_links = [f"/image/{storeid}/{file}" for file in files]
        return {"images": image_links}
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to list images")