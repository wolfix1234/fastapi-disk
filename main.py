from fastapi import FastAPI
from app.api import store, json_api, image, images

app = FastAPI(title="Store Management API")

app.include_router(store.router)
app.include_router(json_api.router)
app.include_router(image.router)
app.include_router(images.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)