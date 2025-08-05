from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.api import store, json_api, image, images
from app.core.config import ALLOWED_ORIGINS

# Configure FastAPI with proper OpenAPI security scheme
app = FastAPI(
    title="Store Management API",
    description="A comprehensive API for managing stores, JSON files, and images with Bearer token authentication",
    version="1.0.0",
    openapi_tags=[
        {"name": "store", "description": "Store management operations"},
        {"name": "json", "description": "JSON file operations"},
        {"name": "image", "description": "Single image operations"},
        {"name": "images", "description": "Multiple image operations"},
    ]
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your bearer token"
        }
    }
    
    # Apply security to all endpoints
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method.lower() != "options":
                openapi_schema["paths"][path][method]["security"] = [{"HTTPBearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(store.router)
app.include_router(json_api.router)
app.include_router(image.router)
app.include_router(images.router)

@app.get("/", tags=["health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Store Management API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is operational"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)