from pydantic import BaseModel, field_validator
from typing import Dict, Any
import json
import re
from app.core.config import FILENAME_PATTERN, MAX_storeId_LENGTH, MAX_JSON_SIZE

class StoreRequest(BaseModel):
    storeId: str
    
    @field_validator('storeId')
    @classmethod
    def validate_storeId(cls, v):
        if not re.match(FILENAME_PATTERN, v) or len(v) > MAX_storeId_LENGTH:
            raise ValueError('Invalid storeId format')
        return v

class JsonUpdateRequest(BaseModel):
    data: Dict[str, Any]
    
    @field_validator('data')
    @classmethod
    def validate_data_size(cls, v):
        if len(json.dumps(v)) > MAX_JSON_SIZE:
            raise ValueError('JSON data too large')
        return v

class DirectJsonRequest(BaseModel):
    model_config = {"extra": "allow"}
    
    def dict(self, **kwargs):
        return super().dict(**kwargs)