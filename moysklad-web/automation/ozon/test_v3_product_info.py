import requests
import json
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

# Try v3 product info endpoint
print("Testing v3/product/info/attributes...")
response = requests.post(
    "https://api-seller.ozon.ru/v3/product/info/attributes",
    headers=headers,
    json={
        "filter": {
            "product_id": [3001140538],
            "visibility": "ALL"
        },
        "limit": 1
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

if response.status_code == 200:
    data = response.json()
    with open('product_attributes_template.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("\n✅ Saved to product_attributes_template.json")
    
    # Extract key info
    if 'result' in data:
        items = data['result']
        if items:
            item = items[0]
            print(f"\nProduct info:")
            print(f"  ID: {item.get('id')}")
            print(f"  Category ID: {item.get('description_category_id')}")
            print(f"  Type ID: {item.get('type_id')}")
            print(f"  Attributes: {len(item.get('attributes', []))}")
