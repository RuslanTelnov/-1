from curl_cffi import requests
import urllib.parse
import re

def search_wb_html(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={encoded_query}"
    
    try:
        print(f"Fetching {url}...")
        response = requests.get(url, impersonate="chrome120", timeout=10)
        if response.status_code == 200:
            html = response.text
            print(f"Page length: {len(html)}")
            
            # Simple regex to find product IDs
            # href="/catalog/123456/detail.aspx"
            ids = re.findall(r'/catalog/(\d+)/detail\.aspx', html)
            unique_ids = list(set(ids))
            print(f"Found {len(unique_ids)} products: {unique_ids[:5]}...")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    search_wb_html("Косметичка текстиль 10X20 см")
