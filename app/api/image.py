from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
from app.utils.validators import validate_filename, safe_path_join
from app.utils.auth import verify_token
from app.core.config import BASE_PATH, MAX_FILE_SIZE, ALLOWED_EXTENSIONS

router = APIRouter(prefix="/image", tags=["image"])

@router.post("/{storeid}")
async def upload_image(storeid: str, file: UploadFile = File(...), token: str = Depends(verify_token)):
    """Upload image to store"""
    image_path = safe_path_join(BASE_PATH, storeid, "image")
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = image_path / unique_filename
    
    try:
        content = await file.read()
        file_path.write_bytes(content)
        return {"message": "Image uploaded", "filename": unique_filename}
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to upload image")

@router.get("/{storeid}/{filename}")
async def get_image(storeid: str, filename: str, token: str = Depends(verify_token)):
    """Get image file"""
    validate_filename(Path(filename).stem)
    image_path = safe_path_join(BASE_PATH, storeid, "image", filename)
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path)

