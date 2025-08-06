from fastapi import APIRouter, HTTPException, Depends
from app.utils.validators import safe_path_join
from app.utils.auth import verify_token
from app.core.config import BASE_PATH

router = APIRouter(prefix="/images", tags=["images"])

@router.get("/{storeId}")
async def list_images(storeId: str, token: str = Depends(verify_token)):
    """List all images in store with detailed information"""
    store_path = safe_path_join(BASE_PATH, storeId)
    image_path = store_path / "image"
    
    if not store_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    if not image_path.exists():
        return {"images": [], "count": 0, "message": "No images directory found"}
    
    try:
        images = []
        for file_path in image_path.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                images.append({
                    "filename": file_path.name,
                    "url": f"/image/{storeId}/{file_path.name}",
                    "size": stat.st_size,
                    "modified": stat.st_mtime
                })
        
        return {
            "images": images,
            "count": len(images),
            "store_id": storeId
        }
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to list images: {str(e)}")