import os
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv('moysklad-web/.env.local')
url = os.environ.get('NEXT_PUBLIC_SUPABASE_URL')
key = os.environ.get('NEXT_PUBLIC_SUPABASE_ANON_KEY')
supabase = create_client(url, key)

# Values to sync
data = {
    "moysklad_login": os.environ.get("MOYSKLAD_LOGIN"),
    "moysklad_password": os.environ.get("MOYSKLAD_PASSWORD"),
    "kaspi_token": "dutmsmqJIEi4CpuX2PNPDLbNcdpiRwNpKc3mwggACq0=", # From chat
    "openai_key": os.environ.get("OPENAI_API_KEY"),
    "rest_api_key": os.environ.get("REST_API_KEY"),
    "kaspi_xml_url": os.environ.get("KASPI_BASE_XML_URL"),
    "retail_divisor": float(os.environ.get("RETAIL_DIVISOR", 0.3)),
    "min_price_divisor": float(os.environ.get("MIN_PRICE_DIVISOR", 0.45)),
    "company_name": "VELVETO"
}

try:
    # Get existing row ID if it exists
    res = supabase.table('client_configs').select('id').limit(1).execute()
    if res.data:
        row_id = res.data[0]['id']
        print(f"Updating existing row {row_id}...")
        supabase.table('client_configs').update(data).eq('id', row_id).execute()
    else:
        print("Inserting new row...")
        supabase.table('client_configs').insert(data).execute()
    print("✅ Successfully synced local configs to Supabase!")
except Exception as e:
    print(f"❌ Error syncing configs: {e}")
