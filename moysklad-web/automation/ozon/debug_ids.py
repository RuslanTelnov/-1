import json
import hashlib
import os

def check_ids():
    input_file = "ozon-automation/products_to_process.json"
    with open(input_file, "r", encoding="utf-8") as f:
        products = json.load(f)
        
    for p in products:
        ms_id = p['ms_id']
        h = hashlib.md5((ms_id + "v3").encode()).hexdigest()
        oid = "".join(filter(str.isdigit, str(int(h, 16))))[:12]
        print(f"{oid}: {p['name']}")

if __name__ == "__main__":
    check_ids()
