import requests
import json
import urllib.parse

def test_wb_search(query):
    # Known WB Search API endpoint
    # Note: 'dest' parameter might depend on region, -1257786 is often used for Moscow/General
    encoded_query = urllib.parse.quote(query)
    url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&query={encoded_query}&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://www.wildberries.ru",
        "Referer": f"https://www.wildberries.ru/catalog/0/search.aspx?search={encoded_query}"
    }
    
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', {}).get('products', [])
            print(f"Found {len(products)} products.")
            
            for p in products[:5]:
                print(f"- {p.get('name')} (Brand: {p.get('brand')})")
                print(f"  ID: {p.get('id')}")
                print(f"  Price: {p.get('salePriceU', 0) / 100} RUB")
                # Construct image URL (WB image logic is complex, but we can try)
                # Usually: https://basket-01.wbbasket.ru/vol{vol}/part{part}/{id}/images/big/1.jpg
                # Need logic to determine basket-XX
                print(f"  Image logic needed for ID {p.get('id')}")
                print("---")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_wb_search("Панама размер универсальный, серый")
