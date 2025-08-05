import requests
import json

BASE_URL = "http://localhost:8000"
TOKEN = "your-secret-token-here"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_store_creation():
    """Test store creation"""
    try:
        response = requests.post(f"{BASE_URL}/store", json={"storeid": "test-store"}, headers=HEADERS)
        print(f"Store creation: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"[ERROR] Store creation failed: {e}")

def test_json_operations():
    """Test JSON operations"""
    storeid = "test-store"
    
    try:
        # Test updating home (lg/sm format)
        test_data = {"test": "data", "updated": True}
        response = requests.post(f"{BASE_URL}/json/{storeid}/home", json={"data": test_data}, headers=HEADERS)
        print(f"Update home JSON: {response.status_code} - {response.json()}")
        
        # Test getting JSON
        response = requests.get(f"{BASE_URL}/json/{storeid}/homelg", headers=HEADERS)
        print(f"Get home JSON: {response.status_code}")
        
        # Test listing JSON files
        response = requests.get(f"{BASE_URL}/json/{storeid}", headers=HEADERS)
        print(f"List JSON files: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"[ERROR] JSON operations failed: {e}")

def test_image_operations():
    """Test image operations"""
    storeid = "test-store"
    
    try:
        # Test listing images
        response = requests.get(f"{BASE_URL}/images/{storeid}", headers=HEADERS)
        print(f"List images: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"[ERROR] Image operations failed: {e}")

def test_unauthorized():
    """Test unauthorized access"""
    try:
        response = requests.get(f"{BASE_URL}/json/test-store")
        print(f"Unauthorized access: {response.status_code} - {response.json()}")
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to server. Make sure it's running on port 8000")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    print("Testing Store Management API...")
    test_unauthorized()
    test_store_creation()
    test_json_operations()
    test_image_operations()
    print("Tests completed!")