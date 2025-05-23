import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_easy_apply_jobs(driver, max_jobs=20):
    job_links = set()
    SCROLL_PAUSE_TIME = 3  # Increased pause time
    
    # Wait for initial job cards to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results__list-item"))
        )
    except TimeoutException:
        print("No job cards found on initial load")
        return list(job_links)

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while len(job_links) < max_jobs:
        # Try multiple selectors for job cards
        selectors = [
            ".jobs-search-results__list-item a[data-control-name='job_card']",
            ".jobs-search-results__list-item a[href*='/jobs/view/']",
            ".jobs-search-results__list-item a[href*='/jobs/']"
        ]
        
        for selector in selectors:
            try:
                cards = driver.find_elements(By.CSS_SELECTOR, selector)
                for card in cards:
                    href = card.get_attribute("href")
                    if href and "/jobs/view/" in href:
                        job_links.add(href)
                    if len(job_links) >= max_jobs:
                        break
            except NoSuchElementException:
                continue
        
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        
        # Check if we've reached the bottom
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # Try one more scroll
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height
        
        print(f"Found {len(job_links)} jobs so far...")

    return list(job_links)
