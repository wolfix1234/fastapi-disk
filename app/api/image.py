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

@router.get("/{storeId}/{filename}")
async def get_image(storeId: str, filename: str):
    """Get image file"""
    image_path = safe_path_join(BASE_PATH, storeId, "image", filename)
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path)

@router.get("/images/{storeId}")
async def list_images(storeId: str):
    """List all images in store"""
    store_path = safe_path_join(BASE_PATH, storeId)
    image_path = store_path / "image"
    
    if not store_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    if not image_path.exists():
        return {"images": []}
    
    images = []
    for file_path in image_path.iterdir():
        if file_path.is_file():
            images.append({
                "filename": file_path.name,
                "url": f"/image/{storeId}/{file_path.name}",
                "size": file_path.stat().st_size
            })
    
    return {"images": images}

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

