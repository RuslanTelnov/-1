import os
import requests
import base64
from dotenv import load_dotenv

# Load Env
load_dotenv("/home/wik/.gemini/antigravity/scratch/wb-dashboard-project/moysklad-automation/.env")

MOYSKLAD_LOGIN = os.getenv('MOYSKLAD_LOGIN')
MOYSKLAD_PASSWORD = os.getenv('MOYSKLAD_PASSWORD')

def get_ms_auth_header():
    auth_str = f"{MOYSKLAD_LOGIN}:{MOYSKLAD_PASSWORD}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()
    return {"Authorization": f"Basic {encoded_auth}"}

def check_product():
    # Search by name part
    name_part = "Альбом Биндер"
    url = f"https://api.moysklad.ru/api/remap/1.2/entity/product?filter=name~{name_part}"
    headers = get_ms_auth_header()
    
    print(f"Searching for: {name_part}")
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        rows = resp.json().get('rows', [])
        print(f"Found {len(rows)} products:")
        for row in rows:
            print(f"Name: {row.get('name')}")
            print(f"Article: {row.get('article')}")
            print(f"Code: {row.get('code')}")
            print("-" * 20)
    else:
        print(f"Error: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    check_product()
