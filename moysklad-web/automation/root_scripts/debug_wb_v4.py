import requests
import json
import sys

def debug_price(nm_id):
    # dest=82 is usually KZ/Astana
    url = f"https://card.wb.ru/cards/v4/detail?appType=1&curr=kzt&dest=82&nm={nm_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching {url}...")
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        products = data.get('data', {}).get('products', [])
        if not products:
            print("No products found in data.")
            return

        p = products[0]
        print(f"Product: {p.get('name')} (Brand: {p.get('brand')})")
        print(f"SalePriceU: {p.get('salePriceU')}")
        
        sizes = p.get('sizes', [])
        if sizes:
            s = sizes[0]
            print(f"Size 0 Price: {s.get('price')}")
        
        # Dump full JSON for inspection
        with open('wb_v4_debug.json', 'w', encoding='utf-8') as f:
            json.dump(p, f, indent=2, ensure_ascii=False)
        print("Saved full dump to wb_v4_debug.json")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Use a known ID or default
    nm_id = 93233379 # Example ID
    if len(sys.argv) > 1:
        nm_id = sys.argv[1]
    debug_price(nm_id)
