import requests
import io
from PIL import Image

BASE_URL = "http://localhost:8000"
TOKEN = "mamad"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def create_test_image(format="PNG"):
    """Create a simple test image in memory"""
    # Create a simple 100x100 colored image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format)
    img_bytes.seek(0)
    return img_bytes

def test_image_upload_and_operations():
    """Test complete image upload workflow"""
    storeid = "test-store"
    
    print("🖼️ Testing Image Upload and Operations...")
    print("-" * 40)
    
    try:
        # Create test PNG image
        test_image = create_test_image("PNG")
        
        # Test image upload
        files = {"file": ("test_image.png", test_image, "image/png")}
        response = requests.post(f"{BASE_URL}/image/{storeid}", files=files, headers=HEADERS)
        print(f"Upload PNG image: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Image uploaded: {result['filename']}")
            uploaded_filename = result['filename']
            
            # Test image retrieval
            response = requests.get(f"{BASE_URL}/image/{storeid}/{uploaded_filename}", headers=HEADERS)
            print(f"Get uploaded image: {response.status_code}")
            
            # Test image listing
            response = requests.get(f"{BASE_URL}/images/{storeid}", headers=HEADERS)
            if response.status_code == 200:
                images = response.json()
                print(f"✅ Images listed: {images['count']} images found")
            
            # Test image deletion
            response = requests.delete(f"{BASE_URL}/image/{storeid}/{uploaded_filename}", headers=HEADERS)
            print(f"Delete image: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Image deleted successfully")
        else:
            print(f"❌ Image upload failed: {response.json()}")
            
    except Exception as e:
        print(f"❌ Image operations failed: {e}")

def test_invalid_file_types():
    """Test uploading invalid file types"""
    storeid = "test-store"
    
    print("\n🚫 Testing Invalid File Types...")
    print("-" * 40)
    
    try:
        # Try to upload a JPEG (not allowed)
        test_image = create_test_image("JPEG")
        files = {"file": ("test_image.jpg", test_image, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/image/{storeid}", files=files, headers=HEADERS)
        print(f"Upload JPEG (should fail): {response.status_code}")
        
        if response.status_code == 400:
            print(f"✅ JPEG correctly rejected: {response.json()['detail']}")
        else:
            print(f"❌ JPEG should have been rejected but got: {response.json()}")
            
        # Try to upload a file with .jpg extension but PNG content
        test_image_png = create_test_image("PNG")
        files = {"file": ("fake.jpg", test_image_png, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/image/{storeid}", files=files, headers=HEADERS)
        print(f"Upload .jpg extension (should fail): {response.status_code}")
        
        if response.status_code == 400:
            print(f"✅ .jpg extension correctly rejected: {response.json()['detail']}")
        else:
            print(f"❌ .jpg extension should have been rejected")
            
    except Exception as e:
        print(f"❌ Invalid file type test failed: {e}")

def test_filename_length_validation():
    """Test filename length validation"""
    print("\n📏 Testing Filename Length Validation...")
    print("-" * 40)
    
    try:
        # Test with long store ID (should fail)
        long_storeid = "a" * 30  # Longer than 25 chars
        response = requests.post(f"{BASE_URL}/store", json={"storeid": long_storeid}, headers=HEADERS)
        print(f"Create store with long ID: {response.status_code}")
        
        if response.status_code == 422:
            print("✅ Long store ID correctly rejected")
        else:
            print("❌ Long store ID should have been rejected")
            
    except Exception as e:
        print(f"❌ Filename validation test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Store Management API - Image & Validation Features")
    print("=" * 60)
    
    test_image_upload_and_operations()
    test_invalid_file_types()
    test_filename_length_validation()
    
    print("\n" + "=" * 60)
    print("✅ Image and validation tests completed!")