# # Store Management API

A comprehensive FastAPI-based REST API for managing stores, JSON files, and images with Bearer token authentication.

## Features

- 🏪 **Store Management**: Create, list, and delete stores
- 📄 **JSON File Operations**: CRUD operations for JSON files with special lg/sm format support
- 🖼️ **Image Management**: Upload, download, list, and delete images
- 🔐 **Bearer Token Authentication**: Secure API access with JWT-style tokens
- 📚 **Interactive Documentation**: Swagger UI with authorization support
- 🌐 **CORS Support**: Cross-origin resource sharing enabled
- ✅ **Input Validation**: Comprehensive request validation and error handling

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python start_server.py
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Authentication

All endpoints require Bearer token authentication. Use the following token:

```
Authorization: Bearer mamad
```

In Swagger UI:
1. Click the "Authorize" button (🔒)
2. Enter: `mamad`
3. Click "Authorize"

## API Endpoints

### Health Check
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Store Management
- `POST /store` - Create a new store
- `GET /store` - List all stores
- `DELETE /store/{storeId}` - Delete a store

### JSON File Operations
- `POST /json/{storeId}/{filename}` - Update JSON file
- `PUT /json/{storeId}/{filename}` - Create new JSON file
- `GET /json/{storeId}/{filename}` - Get JSON file content
- `DELETE /json/{storeId}/{filename}` - Delete JSON file
- `GET /json/{storeId}` - List all JSON files in store

### Image Management
- `POST /image/{storeId}` - Upload image
- `GET /image/{storeId}/{filename}` - Download image
- `DELETE /image/{storeId}/{filename}` - Delete image
- `GET /images/{storeId}` - List all images in store

## Usage Examples

### Create a Store
```bash
curl -X POST "http://localhost:8000/store" \
  -H "Authorization: Bearer mamad" \
  -H "Content-Type: application/json" \
  -d '{"storeId": "my-store"}'
```

### Upload JSON Data
```bash
curl -X POST "http://localhost:8000/json/my-store/home" \
  -H "Authorization: Bearer mamad" \
  -H "Content-Type: application/json" \
  -d '{"data": {"title": "Welcome", "content": "Hello World"}}'
```

### Upload Image
```bash
curl -X POST "http://localhost:8000/image/my-store" \
  -H "Authorization: Bearer mamad" \
  -F "file=@image.png"
```

## Special Features

### Special JSON Files
The following filenames automatically create both `lg` and `sm` versions:
- home, about, blog, blogdetail, collection, contact, detail, juju, store

Example: Updating `home` creates both `homelg.json` and `homesm.json`

### File Validation
- **Store IDs**: Alphanumeric, hyphens, underscores only (max 50 chars)
- **Filenames**: Alphanumeric, hyphens, underscores only (max 50 chars)
- **Images**: JPG, JPEG, PNG, GIF, WEBP (max 10MB)
- **JSON**: Max 1MB per file

## Project Structure

```
fastapi-disk/
├── app/
│   ├── api/           # API route handlers
│   ├── core/          # Configuration
│   ├── models/        # Pydantic schemas
│   └── utils/         # Utilities (auth, validation)
├── data/
│   └── stores/        # Store data directory
├── template/          # JSON templates
├── main.py           # FastAPI application
├── start_server.py   # Server startup script
└── test_api.py       # API tests
```

## Testing

Run the test suite:
```bash
python test_api.py
```

## Configuration

Edit `app/core/config.py` to customize:
- File size limits
- Allowed file extensions
- Authentication token
- CORS origins
- Storage paths

## Security

- Bearer token authentication on all endpoints
- Path traversal protection
- File type validation
- Size limits on uploads
- Input sanitization

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid token)
- `404` - Not Found
- `409` - Conflict (resource already exists)
- `413` - Payload Too Large
- `500` - Internal Server Error

A FastAPI application for managing stores with JSON configuration files and image uploads.

## Features

- Store creation with automatic directory structure
- JSON file management with lg/sm format support
- Image upload and retrieval
- Bearer token authentication
- Kubernetes/Pod ready with shared disk support

## Authentication

All endpoints require Bearer token authentication:
```
Authorization: Bearer your-secret-token-here
```

## API Endpoints

### Store API
- `POST /store` - Create store with directory structure

### JSON API
- `POST /json/{storeId}/{filename}` - Update JSON file
- `GET /json/{storeId}/{filename}` - Get JSON file content
- `PUT /json/{storeId}/{filename}` - Create new JSON file
- `DELETE /json/{storeId}/{filename}` - Delete JSON file
- `GET /json/{storeId}` - List all JSON files

### Image API
- `POST /image/{storeId}` - Upload image
- `GET /image/{storeId}/{filename}` - Get image file
- `GET /images/{storeId}` - List all image links

## Special JSON Handling

For files named: `home`, `about`, `blog`, `blogdetail`, `collection`, `contact`, `detail`, `juju`, `store`

The API automatically handles both `{filename}lg.json` and `{filename}sm.json` formats.

## Running the Application

### Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Docker
```bash
docker build -t store-api .
docker run -p 8000:8000 -v ./data:/data/stores store-api
```

### Docker Compose
```bash
docker-compose up -d
```

## Kubernetes Deployment

Mount shared disk to `/data/stores` in the pod for persistent storage across replicas.

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.