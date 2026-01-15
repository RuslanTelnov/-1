
from curl_cffi import requests
import re

def test_fetch(nm_id):
    # url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={nm_id}"
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&nm={nm_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://www.wildberries.ru",
        "Referer": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx"
    }
    
    impersonations = ["chrome120", "safari15_3", "edge101"]
    
    for imp in impersonations:
        try:
            print(f"\nTesting with impersonation: {imp}")
            response = requests.get(url, headers=headers, impersonate=imp)
            print(f"API Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                products = data.get("data", {}).get("products", [])
                if products:
                    product = products[0]
                    print(f"API Success! Name: {product.get('name')}")
                    print(f"Price U: {product.get('salePriceU')}")
                    break
                else:
                    print("API returned 200 but no products found.")
            else:
                print("API failed.")
        except Exception as e:
            print(f"Error with {imp}: {e}")

    # Test HTML fetch with best impersonation (or last one)
    try:
        print("\nTesting HTML Fetch...")
        html_url = f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx"
        response_html = requests.get(html_url, headers=headers, impersonate="chrome120")
        print(f"HTML Status Code: {response_html.status_code}")
        if "Чехол" in response_html.text or "Samsung" in response_html.text:
            print("HTML Fetch Success! Found product keywords.")
        else:
            print("HTML Fetch Failed (content might be blocked or dynamic).")
            # print(response_html.text[:500])

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fetch(146070400)
