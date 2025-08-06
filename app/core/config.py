from pathlib import Path
import os

# Storage configuration
BASE_PATH = Path("./data/stores").resolve()
TEMPLATE_PATH = Path("template").resolve()

# File size limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_JSON_SIZE = 1024 * 1024  # 1MB

# Allowed file extensions
ALLOWED_EXTENSIONS = {".png", ".webp"}

# Validation patterns
FILENAME_PATTERN = r'^[a-zA-Z0-9_-]+$'
MAX_FILENAME_LENGTH = 25
MAX_storeId_LENGTH = 25

# Authentication
BEARER_TOKEN = "mamad"