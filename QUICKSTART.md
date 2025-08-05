# Quick Start Guide

## 🚀 Start the API Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or use the startup script
python start_server.py
```

## 📖 API Documentation

Visit: **http://localhost:8000/docs**

## 🔑 Authentication

All endpoints require Bearer token:
```
Authorization: Bearer your-secret-token-here
```

## 🧪 Test the API

```bash
# Run the test script (server must be running)
python test_api.py

# Or test manually with curl:
curl -H "Authorization: Bearer your-secret-token-here" \
     -X POST http://localhost:8000/store \
     -H "Content-Type: application/json" \
     -d '{"storeid": "my-store"}'
```

## 📁 API Endpoints

- **POST /store** - Create store
- **POST /json/{storeid}/{filename}** - Update JSON
- **GET /json/{storeid}/{filename}** - Get JSON
- **PUT /json/{storeid}/{filename}** - Create JSON
- **DELETE /json/{storeid}/{filename}** - Delete JSON
- **GET /json/{storeid}** - List JSON files
- **POST /image/{storeid}** - Upload image
- **GET /image/{storeid}/{filename}** - Get image
- **GET /images/{storeid}** - List images

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t store-api .
docker run -p 8000:8000 -v ./data:/data/stores store-api
```