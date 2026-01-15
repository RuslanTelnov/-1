
import os
import json
from dotenv import load_dotenv
from supabase import create_client

# Import the creator function
# We need to add path to sys
import sys
sys.path.append(os.path.join(os.getcwd(), 'moysklad-automation'))
import create_wb_products_in_ms as ms_creator

load_dotenv("moysklad-web/.env.local")

url = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

supabase = create_client(url, key)

# Fetch one errored item
response = supabase.table("wb_search_results").select("*").eq("id", 41166242).limit(1).execute()
if not response.data:
    print("No errored items found.")
    exit()

product = response.data[0]
print(f"Debugging Product: {product['name']} (ID: {product['id']})")
print(f"Price from DB: {product['price_kzt']} (Type: {type(product['price_kzt'])})")

# Prepare data as conveyor does
prod_data = {
    "id": product['id'],
    "name": product['name'],
    "price": int(product.get('price_kzt', 0) or 0),
    "image_url": product.get('image_url')
}

print(f"Computed Price Int: {prod_data['price']}")

# Setup MS Context
folder_meta = ms_creator.get_or_create_group("Parser WB")
price_type_meta = ms_creator.get_price_type("Цена продажи")

# Fetch Preorder Attribute manually to match conveyor
def get_preorder_attribute_beta(headers):
    """Find the 'Предзаказ' attribute meta"""
    url = f"{ms_creator.BASE_URL}/entity/product/metadata/attributes"
    try:
        resp = ms_creator.requests.get(url, headers=headers)
        if resp.status_code == 200:
            rows = resp.json().get('rows', [])
            for row in rows:
                if "предзаказ" in row['name'].lower():
                    print(f"Found Preorder attribute: {row['name']} ({row['id']})")
                    return row['meta']
    except Exception as e:
        print(f"Error finding preorder: {e}")
    return None

preorder_meta = get_preorder_attribute_beta(ms_creator.HEADERS)
extra_attrs = []
if preorder_meta:
    extra_attrs.append({
        "meta": preorder_meta,
        "value": 30
    })

import random
rdm = random.randint(1000000, 9999999)
prod_data['id'] = rdm
prod_data['name'] += f" TEST {rdm}"
print(f"--- Calling Creator with Attributes (New Item {rdm}) ---")
ms_creator.create_product_in_ms(prod_data, folder_meta, price_type_meta, extra_attributes=extra_attrs)
