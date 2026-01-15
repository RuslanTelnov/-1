from curl_cffi import requests
import time
import json

def get_basket_number(nm_id):
    vol = nm_id // 100000
    part = nm_id // 1000
    return vol, part

def test_static_json(nm_id):
    vol, part = get_basket_number(nm_id)
    print(f"NM ID: {nm_id}, Vol: {vol}, Part: {part}")
    
    # Known working host for 179790764
    host = "basket-12.wbbasket.ru"
    nm_id = 179790764
    vol, part = get_basket_number(nm_id)
    
    files = [
        "info/ru/card.json",
        "info/ru/data.json",
        "info/ru/price.json",
        "info/price.json",
        "info/price-history.json",
        "info/ru/sizes.json",
        "info/sizes.json"
    ]
    
    for filename in files:
        url = f"https://{host}/vol{vol}/part{part}/{nm_id}/{filename}"
        try:
            print(f"Testing {url}...")
            response = requests.get(url, timeout=2)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"SUCCESS: {filename}")
                # Save it
                safe_name = filename.replace("/", "_")
                with open(f"wb_{safe_name}", "w") as f:
                    f.write(response.text)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    test_static_json(139833762)
