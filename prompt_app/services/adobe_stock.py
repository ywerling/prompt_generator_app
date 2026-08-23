import time
from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class AdobeScrapingError(RuntimeError):
    """Raised when Adobe does not make search results available to Selenium."""


def create_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(options=options)


def scrape_image_descriptions(query, search_base_url, timeout=20, limit=100):
    query = (query or "").strip()
    if not query:
        return []
    driver = create_webdriver()
    try:
        driver.get(f"{search_base_url}?{urlencode({'k': query})}")
        WebDriverWait(driver, timeout).until(
            lambda browser: browser.execute_script("return document.readyState") == "complete"
        )
        selector = (
            "img[alt]:not([alt='']), "
            "[role='img'][aria-label]:not([aria-label='']), "
            "a[href*='/images/'][aria-label]:not([aria-label=''])"
        )
        deadline = time.monotonic() + timeout
        elements = []
        while time.monotonic() < deadline:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                break
            driver.execute_script("window.scrollBy(0, 800)")
            time.sleep(0.5)
        if not elements:
            title = driver.title or "untitled page"
            raise AdobeScrapingError(
                "Adobe did not provide image results to the automated browser "
                f"(page: {title}). It may be showing a consent, region, CAPTCHA, or bot-protection page."
            )
        descriptions = []
        seen = set()
        for element in elements:
            description = (element.get_attribute("alt") or element.get_attribute("aria-label") or "").strip()
            if len(description) > 1 and description not in seen:
                descriptions.append(description)
                seen.add(description)
            if len(descriptions) == limit:
                break
        return descriptions
    finally:
        driver.quit()
