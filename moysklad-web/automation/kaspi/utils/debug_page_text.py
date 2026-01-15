from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import sys
import time

def dump_text(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(5) # Wait for load
        
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print("--- BODY TEXT START ---")
        print(body_text)
        print("--- BODY TEXT END ---")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    url = sys.argv[1]
    dump_text(url)
