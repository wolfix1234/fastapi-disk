from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
from app.utils.validators import validate_filename, safe_path_join
from app.utils.auth import verify_token
from app.core.config import BASE_PATH, MAX_FILE_SIZE, ALLOWED_EXTENSIONS

router = APIRouter(prefix="/image", tags=["image"])

@router.post("/{storeId}")
async def upload_image(storeId: str, file: UploadFile = File(...), token: str = Depends(verify_token)):
    """Upload image to store"""
    store_path = safe_path_join(BASE_PATH, storeId)
    image_path = store_path / "image"
    
    if not store_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    # Create image directory if it doesn't exist
    if not image_path.exists():
        try:
            image_path.mkdir(parents=True, exist_ok=True)
        except OSError:
            raise HTTPException(status_code=500, detail="Failed to create image directory")
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Check file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB")
    
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = image_path / unique_filename
    
    try:
        file_path.write_bytes(content)
        return {
            "message": "Image uploaded successfully", 
            "filename": unique_filename,
            "size": len(content),
            "url": f"/image/{storeId}/{unique_filename}"
        }
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

# More specific route first to avoid conflicts
@router.get("/images/{storeId}")
async def list_images(storeId: str, token: str = Depends(verify_token)):
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
            "images": images
        }
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to list images: {str(e)}")

# Generic route last to avoid matching the specific routes above
@router.get("/{storeId}/{filename}")
async def get_image(storeId: str, filename: str):
    """Get image file"""
    image_path = safe_path_join(BASE_PATH, storeId, "image", filename)
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path)


@router.delete("/{storeId}/{filename}")
async def delete_image(storeId: str, filename: str, token: str = Depends(verify_token)):
    """Delete image file"""
    image_path = safe_path_join(BASE_PATH, storeId, "image", filename)
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        image_path.unlink()
        return {"message": f"Image {filename} deleted successfully"}
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}")