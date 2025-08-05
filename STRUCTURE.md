# Project Structure

```
disk-vps/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── store.py          # Store creation endpoints
│   │   ├── json_api.py       # JSON CRUD operations
│   │   └── image.py          # Image upload/retrieval
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py         # Configuration constants
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        # Pydantic models
│   └── utils/
│       ├── __init__.py
│       └── validators.py     # Validation utilities
├── template/                 # JSON template files
├── main.py                   # FastAPI app entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## File Responsibilities

- **main.py**: FastAPI app initialization and router registration
- **app/core/config.py**: All configuration constants and settings
- **app/models/schemas.py**: Pydantic request/response models
- **app/utils/validators.py**: Input validation and security utilities
- **app/api/store.py**: Store creation API endpoints
- **app/api/json_api.py**: JSON file management endpoints
- **app/api/image.py**: Image upload and retrieval endpoints