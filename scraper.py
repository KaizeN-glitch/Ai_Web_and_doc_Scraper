from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def scrape_website(website):
    print("Launching Chrome browser...")

    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        html = driver.page_source

        # Crawl linked pages (one level deep)
        linked_html = scrape_linked_pages(driver, website)
        return html + "\n" + linked_html

    finally:
        driver.quit()


def scrape_linked_pages(driver, base_url):
    """Fetch HTML from anchor tags one-level deep"""
    soup = BeautifulSoup(driver.page_source, "html.parser")
    anchors = soup.find_all("a", href=True)
    collected_html = ""
    visited = set()

    for a in anchors[:10]:  # limit to first 10 links to avoid overload
        href = a['href']
        full_url = urljoin(base_url, href)

        if full_url not in visited and base_url.split("//")[1].split("/")[0] in full_url:
            visited.add(full_url)
            try:
                driver.get(full_url)
                time.sleep(2)
                collected_html += driver.page_source + "\n"
            except:
                continue
    
    return collected_html
