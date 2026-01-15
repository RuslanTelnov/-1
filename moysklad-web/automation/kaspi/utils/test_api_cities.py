import requests
import os
import sys

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
    
    url = f"{config.KASPI_MERCHANT_API_URL}/cities"
    
    print(f"Testing connection to {url}...")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}") # Print first 500 chars
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
