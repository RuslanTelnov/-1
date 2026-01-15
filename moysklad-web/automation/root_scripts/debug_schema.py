import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv("moysklad-web/.env.local")

url: str = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
key: str = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")

# Execute migration
try:
    with open("database_migration/add_conveyor_columns.sql", "r") as f:
        sql = f.read()
    # supabase-py doesn't support raw SQL easily unless via specific rpc or if enabled. 
    # But we can try requests to valid backend or use a python utility if we have one.
    # Actually, simpler to just use specific python loop to add columns if not using raw sql.
    # OR we can use the `apply_sql.py` pattern if it exists.
    pass
except Exception as e:
    print(e)

# Let's create a python script to run this SQL via our Supabase client or simply via psycopg2 if available?
# Actually wait, `apply_sql.py` was seen in the file list. Let's use it.


def inspect_table(table_name):
    print(f"--- Schema for {table_name} ---")
    try:
        # Fetch 1 row to see keys
        response = supabase.table(table_name).select("*").limit(1).execute()
        if response.data and len(response.data) > 0:
            print(json.dumps(list(response.data[0].keys()), indent=2))
        else:
            print("(Table empty or error)")
    except Exception as e:
        print(f"Error: {e}")

inspect_table("wb_top_products")
inspect_table("products")
inspect_table("wb_search_results")
