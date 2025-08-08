from fastapi import APIRouter, HTTPException, Depends
from app.utils.validators import safe_path_join
from app.utils.auth import verify_token
from app.core.config import BASE_PATH
from pathlib import Path

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/{storeId}")
async def list_images(storeId: str):
    """
    List all images in a store with detailed information.
    """
    store_path: Path = safe_path_join(BASE_PATH, storeId)

    if not store_path.exists() or not store_path.is_dir():
        raise HTTPException(status_code=404, detail="Store not found")

    image_path = store_path / "image"

    if not image_path.exists() or not image_path.is_dir():
        return {"images": [], "count": 0, "storeId": storeId}

    try:
        images = []
        for file_path in image_path.iterdir():
            if file_path.is_file():
                images.append({
                    "_id": file_path.name,
                    "fileName": file_path.name,
                    "fileUrl": f"/image/{storeId}/{file_path.name}",
                    "storeId": storeId
                })

        return {
            "images": images,
            # "count": len(images),
            # "storeId": storeId
        }
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to list images: {str(e)}")
