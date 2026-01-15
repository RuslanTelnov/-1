from curl_cffi import requests
import json

def test_ozon_mobile():
    # Endpoint often used by mobile app
    url = "https://api.ozon.ru/composer-api.bx/page/json/v2?url=/product/1710393028"
    
    headers = {
        "User-Agent": "ozonapp_android/16.14.0+1658", # Example mobile UA
        "x-o3-app-name": "ozonapp_android",
        "x-o3-app-version": "16.14.0(1658)"
    }
    
    print(f"Testing Mobile API: {url}")
    try:
        # Note: impersonate might conflict with custom headers, so we might try without it or with a specific one
        resp = requests.get(url, headers=headers, impersonate="chrome110", timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print("Success!")
            print(resp.text[:500])
        else:
            print("Failed")
            print(resp.text[:200])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ozon_mobile()
