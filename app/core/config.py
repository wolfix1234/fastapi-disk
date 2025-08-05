from pathlib import Path
import os

# Storage configuration
BASE_PATH = Path("d:/company/fastapi-disk/data/stores").resolve()
TEMPLATE_PATH = Path("d:/company/fastapi-disk/template").resolve()

# File size limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_JSON_SIZE = 1024 * 1024  # 1MB

# Allowed file extensions
ALLOWED_EXTENSIONS = {".png", ".webp"}

# Special files that need lg/sm format
SPECIAL_FILES = {"home", "about", "blog", "blogdetail", "collection", "contact", "detail", "juju", "store"}

# Validation patterns
FILENAME_PATTERN = r'^[a-zA-Z0-9_-]+$'
MAX_FILENAME_LENGTH = 25
MAX_STOREID_LENGTH = 25

# Authentication
BEARER_TOKEN = "mamad"

# CORS settings
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]