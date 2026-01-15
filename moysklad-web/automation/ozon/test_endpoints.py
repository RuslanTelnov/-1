import requests
import os
from dotenv import load_dotenv

load_dotenv('.env.ozon')

OZON_CLIENT_ID = os.getenv('OZON_CLIENT_ID')
OZON_API_KEY = os.getenv('OZON_API_KEY')

headers = {
    'Client-Id': OZON_CLIENT_ID,
    'Api-Key': OZON_API_KEY,
    'Content-Type': 'application/json'
}

print(f"Testing with Client ID: {OZON_CLIENT_ID}")
print(f"API Key: {OZON_API_KEY[:10]}...")
print()

# Try different endpoints
endpoints = [
    ("POST", "/v2/product/list", {"filter": {}, "limit": 1}),
    ("POST", "/v3/product/list", {"filter": {}, "limit": 1}),
    ("POST", "/v1/product/list", {"filter": {}, "limit": 1}),
    ("GET", "/v1/product/info", {}),
]

for method, endpoint, payload in endpoints:
    print(f"Testing {method} {endpoint}...")
    try:
        if method == "POST":
            response = requests.post(
                f"https://api-seller.ozon.ru{endpoint}",
                headers=headers,
                json=payload,
                timeout=10
            )
        else:
            response = requests.get(
                f"https://api-seller.ozon.ru{endpoint}",
                headers=headers,
                timeout=10
            )
        
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        print()
        
        if response.status_code == 200:
            print("✅ SUCCESS! This endpoint works!")
            break
    except Exception as e:
        print(f"  Error: {e}")
        print()
