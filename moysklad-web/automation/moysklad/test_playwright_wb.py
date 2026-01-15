from playwright.sync_api import sync_playwright
import re

def test_wb_price():
    nm_id = 179790764
    url = f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Navigating to {url}...")
        page.goto(url, timeout=60000)
        
        print(f"Page title: {page.title()}")
        
        # Try multiple selectors
        selectors = [
            ".price-block__final-price",
            ".price-block__wallet-price",
            ".product-page__price-block",
            "span.price-block__price"
        ]
        
        found = False
        for selector in selectors:
            try:
                print(f"Trying selector: {selector}")
                page.wait_for_selector(selector, timeout=5000)
                price_text = page.inner_text(selector)
                print(f"Found price text: {price_text}")
                found = True
                break
            except:
                continue
                
        if not found:
            print("Price not found with any selector.")
            page.screenshot(path="wb_error.png")
            
        browser.close()

if __name__ == "__main__":
    test_wb_price()
