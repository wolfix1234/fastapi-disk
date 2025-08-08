from fastapi import APIRouter, HTTPException, Depends
from pathlib import Path
import shutil
from app.models.schemas import StoreRequest
from app.utils.validators import safe_path_join
from app.utils.auth import verify_token
from app.core.config import BASE_PATH, TEMPLATE_PATH

router = APIRouter(prefix="/store", tags=["store"])

@router.post("/")
async def create_store(request: StoreRequest, token: str = Depends(verify_token)):
    """Create store directory structure and copy template files"""
    store_path = safe_path_join(BASE_PATH, request.storeId)
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

        return {"message": f"Store {request.storeId} created successfully"}
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to create store: {str(e)}")
    
@router.get("")
async def list_stores(token: str = Depends(verify_token)):
    """List all available stores"""
    try:
        if not BASE_PATH.exists():
            BASE_PATH.mkdir(parents=True, exist_ok=True)
            return {"stores": [], "count": 0}
        
        stores = []
        for store_path in BASE_PATH.iterdir():
            if store_path.is_dir():
                json_path = store_path / "json"
                image_path = store_path / "image"
                
                json_count = len(list(json_path.glob("*.json"))) if json_path.exists() else 0
                image_count = len([f for f in image_path.iterdir() if f.is_file()]) if image_path.exists() else 0
                
                stores.append({
                    "store_id": store_path.name,
                    "json_files": json_count,
                    "images": image_count,
                    "created": store_path.stat().st_ctime
                })
        
        return {"stores": stores, "count": len(stores)}
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to list stores: {str(e)}")

@router.delete("/{storeId}")
async def delete_store(storeId: str, token: str = Depends(verify_token)):
    """Delete a store and all its contents"""
    store_path = safe_path_join(BASE_PATH, storeId)
    
    if not store_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    try:
        import shutil
        shutil.rmtree(store_path)
        return {"message": f"Store {storeId} deleted successfully"}
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete store: {str(e)}")