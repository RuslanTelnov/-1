from curl_cffi import requests

def test_variations():
    nm_id = 608707482
    dest = -1257786
    
    urls = [
        f"https://card.wb.ru/cards/v1/detail?appType=1&curr=kzt&dest={dest}&spp=30&nm={nm_id}",
        f"https://card.wb.ru/cards/v2/detail?appType=1&curr=kzt&dest={dest}&spp=30&nm={nm_id}",
        f"https://card.wb.ru/cards/detail?appType=1&curr=kzt&dest={dest}&spp=30&nm={nm_id}",
        f"https://card.wb.ru/cards/v1/detail?appType=1&curr=kzt&dest={dest}&nm={nm_id}",
        f"https://card.wb.ru/cards/v2/detail?appType=1&curr=kzt&dest={dest}&nm={nm_id}",
        # Try with semicolon
        f"https://card.wb.ru/cards/v1/detail?appType=1&curr=kzt&dest={dest}&spp=30&nm={nm_id};",
        f"https://card.wb.ru/cards/v2/detail?appType=1&curr=kzt&dest={dest}&spp=30&nm={nm_id};",
    ]
    
    for url in urls:
        print(f"Testing: {url}")
        try:
            resp = requests.get(url, impersonate="chrome110", timeout=5)
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                print("SUCCESS!")
                print(resp.json())
                break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_variations()
