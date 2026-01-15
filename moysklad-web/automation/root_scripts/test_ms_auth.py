
import os
import requests
import base64
from dotenv import load_dotenv

# Try loading from the same path as the real script
load_dotenv("moysklad-web/.env.local")

LOGIN = os.getenv("MOYSKLAD_LOGIN")
PASSWORD = os.getenv("MOYSKLAD_PASSWORD")

print(f"Loaded LOGIN: {LOGIN}")
# Mask password for security in output
masked_pwd = PASSWORD[:2] + "***" if PASSWORD else "None"
print(f"Loaded PASSWORD: {masked_pwd}")

if not LOGIN or not PASSWORD:
    print("❌ Credentials missing in .env.local")
    exit(1)

BASE_URL = "https://api.moysklad.ru/api/remap/1.2"
auth_str = f"{LOGIN}:{PASSWORD}"
auth_b64 = base64.b64encode(auth_str.encode()).decode()
headers = {
    "Authorization": f"Basic {auth_b64}",
    "Content-Type": "application/json"
}

try:
    resp = requests.get(f"{BASE_URL}/entity/product", headers=headers, params={"limit": 1})
    if resp.status_code == 200:
        print("✅ Auth SUCCESS! MoySklad API is accessible.")
        print(f"Found {resp.json()['meta']['size']} products.")
    else:
        print(f"❌ Auth FAILED. Status: {resp.status_code}")
        print(f"Response: {resp.text}")
except Exception as e:
    print(f"❌ Connection Error: {e}")
