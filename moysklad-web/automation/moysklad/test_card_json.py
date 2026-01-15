import requests

def get_basket_number(wb_id):
    vol = wb_id // 100000
    if 0 <= vol <= 143: return "01"
    if 144 <= vol <= 287: return "02"
    if 288 <= vol <= 431: return "03"
    if 432 <= vol <= 719: return "04"
    if 720 <= vol <= 1007: return "05"
    if 1008 <= vol <= 1061: return "06"
    if 1062 <= vol <= 1115: return "07"
    if 1116 <= vol <= 1169: return "08"
    if 1170 <= vol <= 1313: return "09"
    if 1314 <= vol <= 1601: return "10"
    if 1602 <= vol <= 1655: return "11"
    if 1656 <= vol <= 1919: return "12"
    if 1920 <= vol <= 2045: return "13"
    if 2046 <= vol <= 2189: return "14"
    if 2190 <= vol <= 2405: return "15"
    if 2406 <= vol <= 2621: return "16"
    if 2622 <= vol <= 2837: return "17"
    if 2838 <= vol <= 3053: return "18"
    if 3054 <= vol <= 3269: return "19"
    if 3270 <= vol <= 3485: return "20"
    if 3486 <= vol <= 3701: return "21"
    return "22"

def test_card_json():
    wb_id = 179790764
    vol = wb_id // 100000
    part = wb_id // 1000
    basket = get_basket_number(wb_id)
    
    url = f"https://basket-{basket}.wbbasket.ru/vol{vol}/part{part}/{wb_id}/info/ru/card.json"
    print(f"Fetching: {url}")
    
    try:
        resp = requests.get(url, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print("Success! Data keys:", data.keys())
            print("Options:", data.get("options", [])[:3])
        else:
            print("Failed to fetch card.json")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_card_json()
