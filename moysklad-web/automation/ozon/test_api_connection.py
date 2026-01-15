import requests
import os
from dotenv import load_dotenv

load_dotenv('.env.ozon')

OZON_CLIENT_ID = os.getenv('OZON_CLIENT_ID')
OZON_API_KEY = os.getenv('OZON_API_KEY')

headers = {
    'Client-Id': OZON_CLIENT_ID,
    'Api-Key': OZON_API_KEY
}

# Test with a simple endpoint - get product list
response = requests.post(
    "https://api-seller.ozon.ru/v2/product/list",
    headers=headers,
    json={
        "filter": {},
        "limit": 1
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
