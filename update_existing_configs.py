import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv('moysklad-web/.env.local')
url = os.environ.get('NEXT_PUBLIC_SUPABASE_URL')
key = os.environ.get('NEXT_PUBLIC_SUPABASE_ANON_KEY')
supabase = create_client(url, key)

data = {
    "moysklad_login": os.environ.get("MOYSKLAD_LOGIN"),
    "moysklad_password": os.environ.get("MOYSKLAD_PASSWORD"),
    "kaspi_token": "dutmsmqJIEi4CpuX2PNPDLbNcdpiRwNpKc3mwggACq0=",
    "openai_key": os.environ.get("OPENAI_API_KEY"),
}

try:
    res = supabase.table('client_configs').select('id').limit(1).execute()
    if res.data:
        row_id = res.data[0]['id']
        supabase.table('client_configs').update(data).eq('id', row_id).execute()
        print(f"✅ Updated existing row {row_id} with real data.")
    else:
        supabase.table('client_configs').insert(data).execute()
        print("✅ Inserted new row with real data.")
except Exception as e:
    print(f"❌ Error: {e}")
