from fastapi import APIRouter, HTTPException, Depends
import json
from app.models.schemas import JsonUpdateRequest
from app.utils.validators import validate_filename, safe_path_join
from app.utils.auth import verify_token
from app.core.config import BASE_PATH, SPECIAL_FILES

router = APIRouter(prefix="/json", tags=["json"])

@router.post("/{storeid}/{filename}")
async def update_json(storeid: str, filename: str, request: JsonUpdateRequest, token: str = Depends(verify_token)):
    """Update JSON file content"""
    validate_filename(filename)
    json_path = safe_path_join(BASE_PATH, storeid, "json")
    
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    try:
        if filename in SPECIAL_FILES:
            lg_file = json_path / f"{filename}lg.json"
            sm_file = json_path / f"{filename}sm.json"
            
            content = json.dumps(request.data, ensure_ascii=False, indent=2)
            lg_file.write_text(content, encoding='utf-8')
            sm_file.write_text(content, encoding='utf-8')
            return {"message": f"Updated {filename}lg.json and {filename}sm.json"}
        else:
            file_path = json_path / f"{filename}.json"
            file_path.write_text(json.dumps(request.data, ensure_ascii=False, indent=2), encoding='utf-8')
            return {"message": f"Updated {filename}.json"}
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to update file")

@router.get("/{storeid}/{filename}")
async def get_json(storeid: str, filename: str, token: str = Depends(verify_token)):
    """Get JSON file content"""
    validate_filename(filename)
    file_path = safe_path_join(BASE_PATH, storeid, "json", f"{filename}.json")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        raise HTTPException(status_code=500, detail="Failed to read file")

@router.put("/{storeid}/{filename}")
async def create_json(storeid: str, filename: str, request: JsonUpdateRequest, token: str = Depends(verify_token)):
    """Create new JSON file"""
    validate_filename(filename)
    json_path = safe_path_join(BASE_PATH, storeid, "json")
    
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    try:
        if filename in SPECIAL_FILES:
            lg_file = json_path / f"{filename}lg.json"
            sm_file = json_path / f"{filename}sm.json"
            
            content = json.dumps(request.data, ensure_ascii=False, indent=2)
            lg_file.write_text(content, encoding='utf-8')
            sm_file.write_text(content, encoding='utf-8')
            return {"message": f"Created {filename}lg.json and {filename}sm.json"}
        else:
            file_path = json_path / f"{filename}.json"
            file_path.write_text(json.dumps(request.data, ensure_ascii=False, indent=2), encoding='utf-8')
            return {"message": f"Created {filename}.json"}
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to create file")

@router.delete("/{storeid}/{filename}")
async def delete_json(storeid: str, filename: str, token: str = Depends(verify_token)):
    """Delete JSON file"""
    validate_filename(filename)
    json_path = safe_path_join(BASE_PATH, storeid, "json")
    
    try:
        if filename in SPECIAL_FILES:
            lg_file = json_path / f"{filename}lg.json"
            sm_file = json_path / f"{filename}sm.json"
            
            lg_file.unlink(missing_ok=True)
            sm_file.unlink(missing_ok=True)
            return {"message": f"Deleted {filename}lg.json and {filename}sm.json"}
        else:
            file_path = json_path / f"{filename}.json"
            if not file_path.exists():
                raise HTTPException(status_code=404, detail="File not found")
            file_path.unlink()
            return {"message": f"Deleted {filename}.json"}
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to delete file")

@router.get("/{storeid}")
async def list_json_files(storeid: str, token: str = Depends(verify_token)):
    """List all JSON files in store"""
    json_path = safe_path_join(BASE_PATH, storeid, "json")
    
    if not json_path.exists():
        raise HTTPException(status_code=404, detail="Store not found")
    
    try:
        files = [f.name for f in json_path.glob("*.json")]
        return {"files": files}
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to list files")