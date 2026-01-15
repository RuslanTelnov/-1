import os
from dotenv import load_dotenv

load_dotenv("moysklad-automation/.env")

login = os.getenv("MOYSKLAD_LOGIN")
password = os.getenv("MOYSKLAD_PASSWORD")

print(f"Login loaded: {bool(login)}")
if login:
    print(f"Login length: {len(login)}")
    
print(f"Password loaded: {bool(password)}")
if password:
    print(f"Password length: {len(password)}")
