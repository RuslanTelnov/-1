import requests
import os
import sys
import json

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def test_connection():
    token = config.KASPI_API_TOKEN
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token,
        "User-Agent": config.USER_AGENT
    }
    
    # Try a simple JSON payload wrapped in a list
    payload = [
        {
            "sku": "TEST-SKU-123",
            "title": "Test Product",
            "description": "Test Description",
            "brand": "Generic",
            "category": "Test Category",
            "attributes": [
                {"code": "color", "value": "red"}
            ]
        }
    ]

    url = f"{config.KASPI_BASE_URL}/shop/api/v2/products/import"
    
    print(f"Testing connection to {url}...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
