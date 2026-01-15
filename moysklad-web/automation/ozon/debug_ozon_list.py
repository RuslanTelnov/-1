import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load Ozon Env
load_dotenv("/home/wik/.gemini/antigravity/scratch/wb-dashboard-project/ozon-automation/.env.ozon")

OZON_CLIENT_ID = os.getenv('OZON_CLIENT_ID')
OZON_API_KEY = os.getenv('OZON_API_KEY')

def list_orders():
    url = "https://api-seller.ozon.ru/v3/posting/fbs/list"
    headers = {
        'Client-Id': OZON_CLIENT_ID,
        'Api-Key': OZON_API_KEY,
        'Content-Type': 'application/json'
    }
    
    # Fetch orders from last 7 days
    since = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    to = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    payload = {
        "dir": "DESC",
        "filter": {
            "since": since,
            "to": to
        },
        "limit": 50
    }
    
    print("Listing orders (awaiting_packaging)...")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code == 200:
            orders = resp.json().get('result', {}).get('postings', [])
            print(f"Found {len(orders)} orders.")
            for o in orders:
                print(f"- {o['posting_number']} ({o['status']}) - {o['in_process_at']}")
        else:
            print(f"Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    list_orders()
