from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import time
import json

def test_product_page():
    wb_id = 179790764 # Known product
    url = f"https://www.wildberries.ru/catalog/{wb_id}/detail.aspx"
    
    with sync_playwright() as p:
        iphone_13 = p.devices['iPhone 13']
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(**iphone_13, locale='ru-RU', timezone_id='Asia/Almaty')
        stealth = Stealth()
        stealth.apply_stealth_sync(context)
        page = context.new_page()
        
        print(f"Visiting {url}...")
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(5)
        
        # Try to find specs
        # On mobile view, specs might be in a different place or require clicking "More"
        # Let's dump the text content of the specs section if we can find it
        
        try:
            # Look for "Characteristics" or similar
            # In mobile web, it might be under a button or section
            # Let's try to find the 'product-params' class or similar
            
            # Check for "О товаре" or "Характеристики"
            # Often hidden under "Развернуть характеристики"
            
            buttons = page.get_by_text("Развернуть характеристики")
            if buttons.count() > 0:
                buttons.first.click()
                time.sleep(1)
            
            specs_table = page.locator("table.product-params__table")
            if specs_table.count() > 0:
                rows = specs_table.locator("tr").all()
                specs = {}
                for row in rows:
                    key = row.locator("th").inner_text().strip()
                    val = row.locator("td").inner_text().strip()
                    specs[key] = val
                print("Specs found:", json.dumps(specs, ensure_ascii=False, indent=2))
            else:
                print("Specs table not found.")
                
            # Try to find gallery images
            # Usually .slide__content img or similar
            images = page.eval_on_selector_all('img', 'imgs => imgs.map(i => i.src)')
            # Filter for basket images
            wb_images = [img for img in images if 'basket' in img and '/big/' in img]
            # Deduplicate
            wb_images = list(set(wb_images))
            print(f"Found {len(wb_images)} images: {wb_images[:3]}...")
            
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="debug_product.png")
            
        browser.close()

if __name__ == "__main__":
    test_product_page()
