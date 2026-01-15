import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_uc_wb():
    print("Starting UC WB Test...")
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = uc.Chrome(options=options, version_main=120) # Try to specify version if needed, or let it auto-detect
        print("Driver created.")
        
        driver.get("https://www.wildberries.ru/catalog/0/search.aspx?search=Панама")
        print("Page loaded.")
        
        # Wait for title
        print(f"Title: {driver.title}")
        
        # Wait for products
        try:
            wait = WebDriverWait(driver, 20)
            # Look for product card class
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))
            print("Found product cards!")
            
            products = driver.find_elements(By.CLASS_NAME, "product-card")
            print(f"Found {len(products)} products.")
            
            if len(products) > 0:
                print(f"First product: {products[0].text[:100]}...")
                
        except Exception as e:
            print(f"Could not find products: {e}")
            print("Page source snippet:")
            print(driver.page_source[:500])
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    test_uc_wb()
