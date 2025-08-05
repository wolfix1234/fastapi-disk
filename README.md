# Store Management API

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
- `POST /json/{storeid}/{filename}` - Update JSON file
- `GET /json/{storeid}/{filename}` - Get JSON file content
- `PUT /json/{storeid}/{filename}` - Create new JSON file
- `DELETE /json/{storeid}/{filename}` - Delete JSON file
- `GET /json/{storeid}` - List all JSON files

### Image API
- `POST /image/{storeid}` - Upload image
- `GET /image/{storeid}/{filename}` - Get image file
- `GET /images/{storeid}` - List all image links

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