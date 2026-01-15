import requests
import json
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

def test_variants():
    token = config.KASPI_API_TOKEN
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token,
        "User-Agent": config.USER_AGENT
    }
    
    # Load payload
    payload_path = os.path.join(config.DATA_DIR, "150510865_payload.json")
    if not os.path.exists(payload_path):
        print("Payload not found!")
        return
        
    with open(payload_path, "r") as f:
        payload = json.load(f)
        
    # Wrap in list
    final_payload = [payload]

    # Variant 1: No V2
    url_v1 = "https://kaspi.kz/shop/api/products/import"
    print(f"--- Testing POST {url_v1} ---")
    try:
        response = requests.post(url_v1, json=final_payload, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Headers: {response.headers}")
        try:
            print(f"Body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
        
    print("\n")

    # Variant 2: V2 (Check headers)
    url_v2 = f"{config.KASPI_MERCHANT_API_URL}/products/import"
    print(f"--- Testing POST {url_v2} ---")
    try:
        response = requests.post(url_v2, json=final_payload, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Headers: {response.headers}")
        try:
            print(f"Body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_variants()
