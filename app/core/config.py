from pathlib import Path
import os

# Storage configuration
BASE_PATH = Path(os.getenv("SHARE_PATH", "./data/stores")).resolve()
TEMPLATE_PATH = Path(os.getenv("TEMPLATE_FOLDER", "template")).resolve()

# File size limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_JSON_SIZE = 10 * 1024 * 1024  # 10MB

# Allowed file extensions
ALLOWED_EXTENSIONS = {".png", ".webp"}

# Validation patterns
FILENAME_PATTERN = r'^[a-zA-Z0-9_-]+$'
MAX_FILENAME_LENGTH = 25
MAX_storeId_LENGTH = 25

# Authentication
BEARER_TOKEN = os.getenv("SECRET_TOKEN", "mamad")