
from playwright.sync_api import sync_playwright
import time

def test_simple():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        url = "https://www.wildberries.ru/catalog/146070400/detail.aspx"
        print(f"Navigating to {url}")
        
        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            
            title = page.title()
            print(f"Title: {title}")
            
            if "Почти готово" in title:
                print("Bot check detected!")
            
            try:
                name = page.inner_text("h1")
                print(f"Name: {name}")
            except:
                print("Name not found")
                
            try:
                price = page.inner_text(".price-block__final-price")
                print(f"Price: {price}")
            except:
                print("Price not found")
                
        except Exception as e:
            print(f"Error: {e}")
            
        browser.close()

if __name__ == "__main__":
    test_simple()
