from curl_cffi import requests

def test_fetch_html(nm_id):
    url = f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }
    
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=headers, impersonate="chrome120", timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("Success! Page content length:", len(response.text))
            if "Почти готово" in response.text or "Just a moment" in response.text:
                print("BLOCKED: Bot check detected in content.")
            else:
                print("Content seems OK (no obvious block).")
                # Save to file for inspection
                with open("wb_test_page.html", "w") as f:
                    f.write(response.text)
                print("Saved to wb_test_page.html")
        else:
            print("Failed to fetch page.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fetch_html(179790764)
