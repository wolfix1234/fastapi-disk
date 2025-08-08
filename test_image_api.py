import requests
import io
from PIL import Image

BASE_URL = "http://localhost:8000"
TOKEN = "mamad"
STORE_ID = "test-store"

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def test_image_api():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # 1. Create store first
    print("1. Creating store...")
    response = requests.post(f"{BASE_URL}/store", 
                           json={"storeId": STORE_ID}, 
                           headers=headers)
    print(f"Store creation: {response.status_code}")
    
    # 2. Upload image
    print("2. Uploading image...")
    test_image = create_test_image()
    files = {"file": ("test.png", test_image, "image/png")}
    response = requests.post(f"{BASE_URL}/image/{STORE_ID}", 
                           files=files, 
                           headers=headers)
    print(f"Upload: {response.status_code}")
    if response.status_code == 200:
        upload_data = response.json()
        filename = upload_data["filename"]
        print(f"Uploaded filename: {filename}")
        
        # 3. Get image (no auth needed)
        print("3. Getting image...")
        response = requests.get(f"{BASE_URL}/image/{STORE_ID}/{filename}")
        print(f"Get image: {response.status_code}")
        
        # 4. List images
        print("4. Listing images...")
        response = requests.get(f"{BASE_URL}/images/{STORE_ID}")
        print(f"List images: {response.status_code}")
        if response.status_code == 200:
            print(f"Images found: {len(response.json()['images'])}")

if __name__ == "__main__":
    test_image_api()