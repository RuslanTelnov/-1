from curl_cffi import requests
import json

def test_wb_api(nm_id):
    # Working URL found via browser: v4 and dest=82 (Kazakhstan/Astana)
    url = f"https://card.wb.ru/cards/v4/detail?appType=1&curr=kzt&dest=82&nm={nm_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        products = data.get('data', {}).get('products', [])
        if products:
            product = products[0]
            print(f"Product: {product.get('name')}")
            # salePriceU is the price with discount in kopecks
            price_raw = product.get('salePriceU', 0)
            print(f"salePriceU: {price_raw} ({price_raw/100} KZT)")
            
            # totalQuantity is often available at the product level
            total_qty = product.get('totalQuantity', 0)
            print(f"Total Quantity (top level): {total_qty}")
            
            # Or sum up from sizes
            sizes = product.get('sizes', [])
            sum_qty = 0
            for size in sizes:
                stocks = size.get('stocks', [])
                for stock in stocks:
                    sum_qty += stock.get('qty', 0)
            print(f"Sum of stocks from sizes: {sum_qty}")
        else:
            print("No product found in 'products' list")
            print(f"Full data: {json.dumps(data, indent=2)}")
    else:
        print(f"Error: {resp.status_code}")

if __name__ == "__main__":
    test_wb_api(179790764) # Example ID from the code
