from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse

def debug_ozon(query):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.ozon.ru/search/?text={encoded_query}&from_global=true"
        print(f"Navigating to {url}")
        driver.get(url)
        time.sleep(5)
        
        with open("ozon_debug.html", "w") as f:
            f.write(driver.page_source)
        print("Saved ozon_debug.html")
        
        driver.save_screenshot("ozon_debug.png")
        print("Saved ozon_debug.png")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_ozon("Панама")
