import requests
import json

BASE_URL = "http://localhost:8000"
TOKEN = "mamad"
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

def test_store_listing():
    """Test store listing"""
    try:
        response = requests.get(f"{BASE_URL}/store", headers=HEADERS)
        print(f"List stores: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"[ERROR] Store listing failed: {e}")

def test_health_endpoints():
    """Test health check endpoints"""
    try:
        # Test root endpoint (no auth required)
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
        
        # Test health endpoint (no auth required)
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"[ERROR] Health endpoints failed: {e}")

def test_openapi_docs():
    """Test OpenAPI documentation endpoints"""
    try:
        # Test OpenAPI schema
        response = requests.get(f"{BASE_URL}/openapi.json")
        print(f"OpenAPI schema: {response.status_code}")
        
        if response.status_code == 200:
            schema = response.json()
            # Check if security scheme is present
            if "components" in schema and "securitySchemes" in schema["components"]:
                print("✅ Security scheme found in OpenAPI schema")
                print(f"Security schemes: {list(schema['components']['securitySchemes'].keys())}")
            else:
                print("❌ Security scheme missing from OpenAPI schema")
        
    except Exception as e:
        print(f"[ERROR] OpenAPI docs test failed: {e}")

def test_unauthorized():
    """Test unauthorized access"""
    try:
        response = requests.get(f"{BASE_URL}/json/test-store")
        print(f"Unauthorized access: {response.status_code} - {response.json()}")
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to server. Make sure it's running on port 8000")
    except Exception as e:
        print(f"[ERROR] {e}")

def test_comprehensive_json_operations():
    """Test comprehensive JSON operations"""
    storeid = "test-store"
    
    try:
        # Test creating a regular JSON file
        test_data = {"name": "Test Product", "price": 29.99, "category": "electronics"}
        response = requests.put(f"{BASE_URL}/json/{storeid}/product", json={"data": test_data}, headers=HEADERS)
        print(f"Create regular JSON: {response.status_code} - {response.json()}")
        
        # Test getting the created file
        response = requests.get(f"{BASE_URL}/json/{storeid}/product", headers=HEADERS)
        print(f"Get regular JSON: {response.status_code}")
        
        # Test deleting the file
        response = requests.delete(f"{BASE_URL}/json/{storeid}/product", headers=HEADERS)
        print(f"Delete regular JSON: {response.status_code} - {response.json()}")
        
    except Exception as e:
        print(f"[ERROR] Comprehensive JSON operations failed: {e}")

if __name__ == "__main__":
    print("🚀 Testing Store Management API...")
    print("=" * 50)
    
    print("\n📋 Testing Health Endpoints...")
    test_health_endpoints()
    
    print("\n📚 Testing OpenAPI Documentation...")
    test_openapi_docs()
    
    print("\n🔒 Testing Unauthorized Access...")
    test_unauthorized()
    
    print("\n🏪 Testing Store Operations...")
    test_store_creation()
    test_store_listing()
    
    print("\n📄 Testing JSON Operations...")
    test_json_operations()
    test_comprehensive_json_operations()
    
    print("\n🖼️ Testing Image Operations...")
    test_image_operations()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")