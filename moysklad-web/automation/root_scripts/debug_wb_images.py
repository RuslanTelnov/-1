import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

res = supabase.table("wb_search_results").select("id, name, image_url").limit(5).execute()
print("Top 5 products in wb_search_results:")
for row in res.data:
    print(f"ID: {row['id']} | Name: {row['name']} | Image URL: {row['image_url']}")
