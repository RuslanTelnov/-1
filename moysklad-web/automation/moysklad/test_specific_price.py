from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import re
import time

def test_fetch_specific_product():
    nm_id = 146070400
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="ru-RU",
            timezone_id="Asia/Almaty",
            is_mobile=False,
            has_touch=False
        )
        
        stealth = Stealth()
        page = context.new_page()
        stealth.apply_stealth_sync(page)
        
        try:
            print("Visiting wildberries.kz...")
            page.goto("https://wildberries.kz/", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            # Navigate to product page
            # url = f"https://global.wildberries.ru/product?card={nm_id}" 
            # Trying global or kz specific url
            # Actually, let's try the standard one but check if it redirects
            url = f"https://www.wildberries.kz/catalog/{nm_id}/detail.aspx"
            print(f"Navigating to: {url}")
            page.goto(url, timeout=90000, wait_until="domcontentloaded")
            
            # Check for bot check
            if "Почти готово" in page.title() or "Just a moment" in page.title():
                print("Bot check detected, waiting...")
                page.wait_for_timeout(10000)
            
            # Save HTML for inspection
            with open("wb_page.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            print("Saved HTML to wb_page.html")
            
            # Initialize variables for metadata
            name = "Unknown"
            rating = 0.0
            feedbacks = 0
            delivery_date = "Unknown"

            # Get name
            if page.query_selector(".product-page__title"):
                name = page.inner_text(".product-page__title")
            elif page.query_selector("h1"):
                 name = page.inner_text("h1")
            
            print(f"Name: {name}")

            # Get Rating and Reviews
            # Try standard selectors first
            if page.query_selector(".product-review__rating"):
                rating_text = page.inner_text(".product-review__rating")
                try:
                    rating = float(rating_text.replace(",", ".").strip())
                except:
                    pass
                    
            if page.query_selector(".product-review__count-review"):
                reviews_text = page.inner_text(".product-review__count-review")
                try:
                    feedbacks = int(re.sub(r'\D', '', reviews_text))
                except:
                    pass
                    
            # Fallback to combined selector
            if rating == 0 and feedbacks == 0:
                combined_selector = ".productReview--Ab1Vp span"
                if page.query_selector(combined_selector):
                    combined_text = page.inner_text(combined_selector)
                    parts = combined_text.split('·')
                    if len(parts) > 0:
                        try:
                            rating = float(parts[0].replace(",", ".").strip())
                        except:
                            pass
                    if len(parts) > 1:
                        try:
                            feedbacks = int(re.sub(r'\D', '', parts[1]))
                        except:
                            pass

            # Get Delivery Date
            if page.query_selector(".product-page__delivery-date"): # Hypothetical selector
                 pass
            
            # Look for text containing month names
            months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
            try:
                # Search for elements containing any month name
                for month in months:
                     element = page.get_by_text(month).first
                     if element.is_visible():
                         delivery_date = element.inner_text()
                         break
            except:
                pass

            print(f"Metadata: Rating={rating}, Reviews={feedbacks}, Delivery={delivery_date}")
            
            # Try 'ins' first
            price_selector = "ins" 
            if not page.query_selector(price_selector):
                price_selector = ".price-block__final-price"
            
            if page.query_selector(price_selector):
                price_text = page.inner_text(price_selector)
                print(f"Raw Price Text: {price_text}")
                
                # Parse currency
                currency = "KZT"
                if "₽" in price_text:
                    currency = "RUB"
                elif "₸" in price_text:
                    currency = "KZT"
                    
                price_clean = re.sub(r'[^\d]', '', price_text)
                price = int(price_clean)
                
                print(f"Parsed: {price} {currency}")
                
                # Metadata Selectors
                # Rating
                rating_selector = ".product-review__rating"
                if page.query_selector(rating_selector):
                    rating = page.inner_text(rating_selector)
                    print(f"Rating: {rating}")
                else:
                    print("Rating selector not found")

                # Reviews
                reviews_selector = ".product-review__count-review"
                if page.query_selector(reviews_selector):
                    reviews = page.inner_text(reviews_selector)
                    print(f"Reviews: {reviews}")
                else:
                    print("Reviews selector not found")
                    
                # Delivery
                # Delivery info is often in a block like .delivery-info or similar
                # It might be dynamic. Let's try to find text containing "достав"
                try:
                    delivery_element = page.locator("text=достав").first
                    if delivery_element:
                        print(f"Delivery Text: {delivery_element.inner_text()}")
                except:
                    print("Delivery text not found")

            else:
                print("Price selector not found")
                page.screenshot(path="debug_error.png")

        except Exception as e:
            print(f"Error: {e}")
        
        browser.close()

if __name__ == "__main__":
    test_fetch_specific_product()
