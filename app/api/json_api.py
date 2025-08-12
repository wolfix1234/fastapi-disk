from fastapi import APIRouter, HTTPException, Depends
import json
from app.models.schemas import DirectJsonRequest
from app.utils.validators import validate_filename, safe_path_join
from app.utils.auth import verify_token
from app.core.config import BASE_PATH
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/json", tags=["json"])



@router.post("/{storeId}/{filename}")
async def update_json(storeId: str, filename: str, data: DirectJsonRequest, token: str = Depends(verify_token)):
    body = data.dict()
    logger.info(f"request body: {body}")
    validate_filename(filename)
    json_path = safe_path_join(BASE_PATH, storeId, "json")

    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")

    try:
        file_path = json_path / f"{filename}.json"
        file_path.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding='utf-8')
        return {"message": f"Updated {filename}.json"}
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to update file")


@router.get("/{storeId}/{filename}")
async def get_json(storeId: str, filename: str, token: str = Depends(verify_token)):
    """Get JSON file content"""
    validate_filename(filename)
    file_path = safe_path_join(BASE_PATH, storeId, "json", f"{filename}.json")
    
    json_path = safe_path_join(BASE_PATH, storeId, "json")
    
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        raise HTTPException(status_code=500, detail="Failed to read file")

@router.put("/{storeId}/{filename}")
async def create_json(
    storeId: str,
    filename: str,
    data: DirectJsonRequest,
    token: str = Depends(verify_token)
):
    """Create new JSON file"""
    body = data.dict()

    validate_filename(filename)
    json_path = safe_path_join(BASE_PATH, storeId, "json")

    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")

    try:
        lg_file = json_path / f"{filename}lg.json"
        sm_file = json_path / f"{filename}sm.json"

        if lg_file.exists() or sm_file.exists():
            raise HTTPException(status_code=409, detail="JSON files already exist")

        content = json.dumps(body, ensure_ascii=False, indent=2)
        lg_file.write_text(content, encoding='utf-8')
        sm_file.write_text(content, encoding='utf-8')

        return {"message": f"Created {filename}lg.json and {filename}sm.json"}
    except OSError as e:
        logger.exception("File creation failed")
        raise HTTPException(status_code=500, detail="Failed to create file")

@router.delete("/{storeId}/{filename}")
async def delete_json(storeId: str, filename: str, token: str = Depends(verify_token)):
    """Delete JSON file"""
    validate_filename(filename)
    json_path = safe_path_join(BASE_PATH, storeId, "json")
    
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    try:
        lg_file = json_path / f"{filename}lg.json"
        sm_file = json_path / f"{filename}sm.json"
        
        if not lg_file.exists() and not sm_file.exists():
            raise HTTPException(status_code=404, detail="Files not found")
        
        lg_file.unlink(missing_ok=True)
        sm_file.unlink(missing_ok=True)
        return {"message": f"Deleted {filename}lg.json and {filename}sm.json"}
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to delete file")

@router.get("/{storeId}")
async def list_json_files(storeId: str, token: str = Depends(verify_token)):
    """List all JSON files in store"""
    json_path = safe_path_join(BASE_PATH, storeId, "json")
    
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    try:
        files = [f.name for f in json_path.glob("*.json")]
        return {"files": files}
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to list files")