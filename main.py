# This script automates the job application process on LinkedIn using Selenium WebDriver with Chrome

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from config import JOB_TITLE, LOCATION, RESUME_PATH
from utils import load_cookies, save_cookies, init_db, already_applied, mark_applied
from job_scraper import get_easy_apply_jobs
from apply_handler import apply_to_job

def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Optional: run headless
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    driver.get("https://www.linkedin.com")

    input("🔐 Log in to LinkedIn manually, then press Enter to continue...")

    save_cookies(driver)
    load_cookies(driver)
    init_db()

    # Search URL with Easy Apply filter
    search_url = (
        f"https://www.linkedin.com/jobs/search/?keywords={JOB_TITLE}"
        f"&location={LOCATION}&f_AL=true&f_WT=2"
    )
    driver.get(search_url)

    # Wait for job cards to appear
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-control-name='job_card']"))
    )

    time.sleep(2)  # Slight delay for safety
    jobs = get_easy_apply_jobs(driver)
    print(f"🔍 Found {len(jobs)} Easy Apply jobs.")

    for job_url in jobs:
        if already_applied(job_url):
            print(f"⏭ Already applied to {job_url}")
            continue
        try:
            applied = apply_to_job(driver, job_url, RESUME_PATH)
            if applied:
                mark_applied(job_url)
                print(f"✅ Applied to {job_url}")
            else:
                print(f"❌ Skipped {job_url} — not Easy Apply or extra steps")
        except Exception as e:
            print(f"⚠️ Error applying to {job_url}: {e}")

    driver.quit()

if __name__ == "__main__":
    main()
