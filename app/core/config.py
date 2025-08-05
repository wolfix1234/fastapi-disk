from pathlib import Path

# Storage configuration
BASE_PATH = "/data/stores"
TEMPLATE_PATH = "template"

# File size limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_JSON_SIZE = 1024 * 1024  # 1MB

# Allowed file extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Special files that need lg/sm format
SPECIAL_FILES = {"home", "about", "blog", "blogdetail", "collection", "contact", "detail", "juju", "store"}

# Validation patterns
FILENAME_PATTERN = r'^[a-zA-Z0-9_-]+$'
MAX_FILENAME_LENGTH = 50
MAX_STOREID_LENGTH = 50

# Authentication
BEARER_TOKEN = "your-secret-token-here"