from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import re
import time

def test_fetch_price(nm_id):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="kk-KZ",
            timezone_id="Asia/Almaty",
            is_mobile=False,
            has_touch=False
        )
        
        stealth = Stealth()
        page = context.new_page()
        stealth.apply_stealth_sync(page)
        
        try:
            print("Visiting wildberries.kz to set region...")
            page.goto("https://wildberries.kz/", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            
            # Try to fetch data using the browser's fetch API
            print("Attempting to fetch data via browser context...")
            api_url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=kzt&dest=-1257786&spp=30&nm={nm_id}"
            
            try:
                data = page.evaluate(f"""async () => {{
                    const response = await fetch('{api_url}');
                    return await response.json();
                }}""")
                
                products = data.get("data", {}).get("products", [])
                if products:
                    product = products[0]
                    price = product.get("salePriceU", 0) / 100
                    name = product.get("name")
                    print(f"API Fetch Success! Name: {name}, Price: {price}")
                else:
                    print("API Fetch returned no products")
                    print(json.dumps(data, indent=2))
            except Exception as e:
                print(f"API Fetch failed: {e}")
                
            # Take a screenshot to see what's happening
            page.screenshot(path="debug_page.png")
            print("Screenshot saved to debug_page.png")
            
            # Try to find price
            print("Searching for price...")
            
            # List of potential selectors
            selectors = [
                "ins",
                ".price-block__final-price",
                ".price-block__wallet-price",
                ".product-page__price-block",
                "text=₸"
            ]
            
            for selector in selectors:
                try:
                    if selector.startswith("text="):
                        element = page.locator(selector).first
                    else:
                        element = page.query_selector(selector)
                        
                    if element:
                        text = element.inner_text() if not selector.startswith("text=") else element.inner_text()
                        print(f"Found selector '{selector}': {text}")
                        if selector == "ins":
                             print(f"Outer HTML: {element.evaluate('el => el.outerHTML')}")
                    else:
                        print(f"Selector '{selector}' not found")
                except Exception as e:
                    print(f"Error checking selector '{selector}': {e}")

        except Exception as e:
            print(f"Error: {e}")
            
        # Save HTML for inspection
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("Saved HTML to debug_page.html")
        
        browser.close()

if __name__ == "__main__":
    # Test with a known product ID
    test_fetch_price(179790764)
