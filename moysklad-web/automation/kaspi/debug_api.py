import requests
import json

token = "dutmsmqJIEi4CpuX2PNPDLbNcdpiRwNpKc3mwggACq0="
headers_base = {
    "X-Auth-Token": token,
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

endpoints = [
    "https://kaspi.kz/shop/api/products/import",
    "https://kaspi.kz/shop/api/v2/products/import",
    "https://kaspi.kz/shop/api/v1/products/import",
    "https://kaspi.kz/shop/api/products/import/attributes",
]

payload = [
    {
        "sku": "WB-123873313",
        "title": "Ролик для пресса Zhebo черный",
        "brand": "Zhebo",
        "category": "Master - Ab rollers",
        "description": "Ролик для пресса Zhebo черный",
        "attributes": [
            {"code": "Ab rollers*Wheels number", "value": "1"},
            {"code": "Ab rollers*Max load", "value": 100},
            {"code": "Ab rollers*Wheels material", "value": ["пластик"]},
            {"code": "Ab rollers*Material", "value": ["металл", "пластик"]},
            {"code": "Ab rollers*Color", "value": "черный"},
            {"code": "Ab rollers*Vendor code", "value": "AB-ROLLER-01"}
        ],
        "images": [{"url": "https://resources.wbstatic.net/tm/new/123870000/123873313-1.jpg"}]
    }
]

for url in endpoints:
    print(f"\n--- Testing {url} ---")
    for method in ["POST", "PUT"]:
        print(f"Method: {method}")
        try:
            if method == "POST":
                resp = requests.post(url, json=payload, headers=headers_base)
            else:
                resp = requests.put(url, json=payload, headers=headers_base)
            
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text[:500]}")
        except Exception as e:
            print(f"Error: {e}")
