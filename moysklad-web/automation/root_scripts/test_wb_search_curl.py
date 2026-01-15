from curl_cffi import requests
import urllib.parse
import json

def test_wb_search(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&query={encoded_query}&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false"
    
    print(f"Fetching {url}...")
    try:
        # impersonate="chrome" mimics a real browser TLS handshake
        response = requests.get(url, impersonate="chrome", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', {}).get('products', [])
            print(f"Found {len(products)} products.")
            
            for p in products[:5]:
                print(f"- {p.get('name')} (Brand: {p.get('brand')})")
                print(f"  ID: {p.get('id')}")
                print(f"  Price: {p.get('salePriceU', 0) / 100} RUB")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_wb_search("Панама")
