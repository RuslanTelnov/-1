import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load Ozon Env
load_dotenv("/home/wik/.gemini/antigravity/scratch/wb-dashboard-project/ozon-automation/.env.ozon")

OZON_CLIENT_ID = os.getenv('OZON_CLIENT_ID')
OZON_API_KEY = os.getenv('OZON_API_KEY')

def get_order_details(posting_number):
    url = "https://api-seller.ozon.ru/v3/posting/fbs/get"
    headers = {
        'Client-Id': OZON_CLIENT_ID,
        'Api-Key': OZON_API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "posting_number": posting_number
    }
    
    print(f"Fetching order: {posting_number}")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code == 200:
            order = resp.json().get('result', {})
            print(json.dumps(order, indent=2, ensure_ascii=False))
        else:
            print(f"Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    get_order_details("0149057327-0241-1")
