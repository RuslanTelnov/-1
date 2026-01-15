import requests
import json
import os
from dotenv import load_dotenv

if os.path.exists(".env.ozon"):
    load_dotenv(".env.ozon")
else:
    load_dotenv(os.path.join(os.getcwd(), "ozon-automation", ".env.ozon"))

OZON_CLIENT_ID = os.getenv('OZON_CLIENT_ID')
OZON_API_KEY = os.getenv('OZON_API_KEY')

headers = {
    'Client-Id': OZON_CLIENT_ID,
    'Api-Key': OZON_API_KEY,
    'Content-Type': 'application/json'
}

def test_v3_attributes(category_id):
    url = "https://api-seller.ozon.ru/v3/category/attribute"
    payload = {
        "description_category_id": [int(category_id)],
        "language": "DEFAULT"
    }
    
    print(f"Fetching v3 attributes for category {category_id}...")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
            print(f"Error: {resp.status_code} - {resp.text}")
            return

        data = resp.json()
        result = data.get('result', [])
        
        for item in result:
             print(f"Category ID: {item.get('description_category_id')}")
             for attr in item.get('attributes', []):
                 print(f"  Attr: {attr['name']} (ID: {attr['id']})")
                 if attr['id'] == 8229: # Type
                     print("  *** FOUND TYPE ATTRIBUTE ***")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    import sys
    cat_id = sys.argv[1] if len(sys.argv) > 1 else "17028706"
    test_v3_attributes(cat_id)
