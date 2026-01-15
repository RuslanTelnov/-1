from curl_cffi import requests
import json
import time

def test_endpoints(nm_id):
    # List of domains to test
    domains = [
        "card.wb.ru",
        "basket-01.wbbasket.ru",
        "basket-02.wbbasket.ru",
        "basket-03.wbbasket.ru",
        "basket-04.wbbasket.ru",
        "basket-05.wbbasket.ru",
        "basket-06.wbbasket.ru",
        "basket-07.wbbasket.ru",
        "basket-08.wbbasket.ru",
        "basket-09.wbbasket.ru",
        "basket-10.wbbasket.ru",
        "www.wildberries.ru"
    ]
    
    # List of paths to test
    paths = [
        f"/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={nm_id}",
        f"/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={nm_id}",
        f"/cards/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={nm_id}",
        # Try without dest
        f"/cards/v1/detail?appType=1&curr=rub&spp=30&nm={nm_id}",
        f"/cards/v2/detail?appType=1&curr=rub&spp=30&nm={nm_id}",
        # Try known working static path to check connectivity
        "/vol0/data/main-menu-ru-ru-v2.json" 
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://www.wildberries.ru",
        "Referer": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx"
    }
    
    for domain in domains:
        for path in paths:
            if "main-menu" in path and domain != "static-basket-01.wbbasket.ru":
                 # Skip main menu check on non-static domains if you want, but let's try all
                 pass
            
            url = f"https://{domain}{path}"
            # Special case for static basket which is known to host menu
            if "main-menu" in path:
                 url = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v2.json"
            
            try:
                print(f"Testing {url}...")
                response = requests.get(url, headers=headers, impersonate="chrome120", timeout=5)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("SUCCESS!")
                    if "main-menu" in path:
                        print("Connectivity check passed.")
                    else:
                        try:
                            data = response.json()
                            products = data.get("data", {}).get("products", [])
                            if products:
                                print(f"Found product: {products[0].get('name')}")
                                print(f"Price: {products[0].get('salePriceU', 0) / 100}")
                                return # Found it!
                            else:
                                print("JSON valid but no products.")
                        except:
                            print("Not JSON or invalid.")
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(0.5)

if __name__ == "__main__":
    test_endpoints(179790764)
