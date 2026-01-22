"""Test API endpoints to diagnose 422 errors"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_login():
    """Test login endpoint"""
    print("\n=== Testing Login ===")
    url = f"{BASE_URL}/auth/login"
    data = {"username": "admin", "password": "admin123"}
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            return response.json().get('access_token')
    except Exception as e:
        print(f"Error: {e}")
    
    return None

def test_dashboard(token):
    """Test dashboard endpoint with token"""
    print("\n=== Testing Dashboard ===")
    url = f"{BASE_URL}/dashboard/metrics?year=2026&month=1"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Headers sent: {headers}")
        
        if response.status_code == 422:
            print("422 Error Response:")
            try:
                print(json.dumps(response.json(), indent=2))
            except:
                print(f"Raw response: {response.text}")
        elif response.status_code == 200:
            print("✓ Success! Dashboard data retrieved")
        else:
            print(f"Response: {response.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

def test_products(token):
    """Test products endpoint with token"""
    print("\n=== Testing Products ===")
    url = f"{BASE_URL}/products?page=1&per_page=10"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 422:
            print("422 Error Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)[:500]}...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("API Endpoint Testing")
    print("=" * 50)
    
    token = test_login()
    
    if token:
        print(f"\n✓ Token received: {token[:30]}...")
        test_dashboard(token)
        test_products(token)
    else:
        print("\n✗ Failed to get token")
