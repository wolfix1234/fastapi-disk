import re
from pathlib import Path
from fastapi import HTTPException
from app.core.config import BASE_PATH, FILENAME_PATTERN, MAX_FILENAME_LENGTH

def validate_filename(filename: str) -> str:
    if not re.match(FILENAME_PATTERN, filename) or len(filename) > MAX_FILENAME_LENGTH:
        raise HTTPException(status_code=400, detail="Invalid filename")
    return filename

def safe_path_join(*args) -> Path:
    path = Path(*args).resolve()
    base_path_str = str(BASE_PATH).lower()
    path_str = str(path).lower()
    if not path_str.startswith(base_path_str):
        raise HTTPException(status_code=400, detail="Invalid path")
    return path