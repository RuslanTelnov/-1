from curl_cffi import requests
import urllib.parse

def test_wb_html_search(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={encoded_query}"
    
    print(f"Fetching {url}...")
    try:
        # impersonate="chrome" mimics a real browser TLS handshake
        response = requests.get(url, impersonate="chrome", timeout=15)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            html = response.text
            print(f"Content Length: {len(html)}")
            
            # Check for product card indicators
            if "product-card" in html or "j-card-item" in html:
                print("SUCCESS: Found product card markers in HTML.")
            else:
                print("WARNING: Did not find product card markers. Page might be dynamic or blocked.")
                # Save to file for inspection
                with open("wb_search_result.html", "w", encoding="utf-8") as f:
                    f.write(html)
                print("Saved wb_search_result.html")
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_wb_html_search("Панама")
