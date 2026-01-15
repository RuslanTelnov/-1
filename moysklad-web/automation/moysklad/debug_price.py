import requests
import json

def get_basket_number(nm_id):
    vol = nm_id // 100000
    part = nm_id // 1000
    return vol, part

from concurrent.futures import ThreadPoolExecutor, as_completed

def check_basket(i, vol, part, nm_id):
    host = f"basket-{i:02d}.wbbasket.ru"
    url = f"https://{host}/vol{vol}/part{part}/{nm_id}/info/ru/card.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, timeout=2, headers=headers)
        if response.status_code == 200:
            return host
    except:
        pass
    return None

def find_basket_host(nm_id):
    vol, part = get_basket_number(nm_id)
    print(f"Searching host for {nm_id} (vol: {vol})...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(check_basket, i, vol, part, nm_id) for i in range(1, 50)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                return result
    return None

nm_id = 150510865
vol, part = get_basket_number(nm_id)
host = find_basket_host(nm_id)

if not host:
    print("Host not found!")
    exit(1)

print(f"Found host: {host}")

# Check price-history.json
price_url = f"https://{host}/vol{vol}/part{part}/{nm_id}/info/price-history.json"
try:
    resp = requests.get(price_url, headers=headers)
    print(f"Price History status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        if isinstance(data, list) and data:
            print("Price History (Last Entry):")
            print(json.dumps(data[-1], indent=2))
except Exception as e:
    print(f"Price History error: {e}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Test KZ dest IDs and known good product
products_to_test = [
    {"id": 608707482, "name": "Problematic Product"},
    {"id": 150510865, "name": "Known Good Product"} 
]

dests = [
    -1257786, # Default/Moscow?
    12358048, # Almaty?
    12358548,
    -1257233,
    -1181050,
    12358536
]

for p in products_to_test:
    print(f"\nTesting {p['name']} ({p['id']})...")
    for dest in dests:
        url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=kzt&dest={dest}&spp=30&nm={p['id']}"
        try:
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                if 'data' in data and 'products' in data['data'] and len(data['data']['products']) > 0:
                    prod = data['data']['products'][0]
                    print(f"  [SUCCESS] dest={dest}: PriceU={prod.get('priceU')}, SalePriceU={prod.get('salePriceU')}")
                else:
                    print(f"  [200 OK, No Data] dest={dest}")
            else:
                print(f"  [Fail {resp.status_code}] dest={dest}")
        except Exception as e:
            print(f"  [Error] dest={dest}: {e}")
try:
    resp = requests.get(price_url, headers=headers)
    print(f"Price History status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        if isinstance(data, list) and data:
            print("Price History (Last Entry):")
            print(json.dumps(data[-1], indent=2))
except Exception as e:
    print(f"Price History error: {e}")
