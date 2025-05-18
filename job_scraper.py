import time
from selenium.webdriver.common.by import By

def get_easy_apply_jobs(driver, max_jobs=20):
    job_links = set()
    SCROLL_PAUSE_TIME = 2

    while len(job_links) < max_jobs:
        cards = driver.find_elements(By.CSS_SELECTOR, "a[data-control-name='job_card']")
        for card in cards:
            href = card.get_attribute("href")
            if href and "/jobs/view/" in href:
                job_links.add(href)
            if len(job_links) >= max_jobs:
                break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

    return list(job_links)
