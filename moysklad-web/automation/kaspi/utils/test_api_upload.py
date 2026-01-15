import requests
import os
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def test_connection():
    token = config.KASPI_API_TOKEN
    headers = {
        "X-Auth-Token": token,
        "User-Agent": config.USER_AGENT
    }
    
    # Simple XML payload
    xml_content = """<?xml version="1.0" encoding="utf-8"?>
<kaspi_catalog date="string" xmlns="kaspiShopping" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="kaspiShopping http://kaspi.kz/kaspishopping.xsd">
    <company>Test Company</company>
    <merchantid>TestID</merchantid>
    <offers>
    </offers>
</kaspi_catalog>"""

    # Create a temporary file
    with open("test_import.xml", "w") as f:
        f.write(xml_content)

    url = f"{config.KASPI_MERCHANT_API_URL}/products/import"
    
    print(f"Testing upload to {url}...")
    try:
        files = {'file': ('test_import.xml', open('test_import.xml', 'rb'), 'application/xml')}
        response = requests.post(url, files=files, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists("test_import.xml"):
            os.remove("test_import.xml")

if __name__ == "__main__":
    test_connection()
