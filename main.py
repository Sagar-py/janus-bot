# This script automates the job application process on LinkedIn using Selenium WebDriver with Chrome

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import urllib.parse
import time
from config import JOB_TITLES, LOCATION, RESUME_PATH, MAX_JOBS_PER_TITLE
from utils import load_cookies, save_cookies, init_db, already_applied, mark_applied
from job_scraper import get_easy_apply_jobs
from apply_handler import apply_to_job

def wait_for_job_cards(driver, timeout=20):
    """Wait for job cards to load with multiple selector attempts"""
    selectors = [
        ".jobs-search-results__list-item",
        ".jobs-search-results-list__item",
        "[data-job-id]",
        ".job-card-container"
    ]
    
    for selector in selectors:
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
            print(f"✅ Found job cards using selector: {selector}")
            return True
        except TimeoutException:
            continue
    
    return False

def search_jobs(driver, job_title):
    """Search for jobs with a specific title"""
    encoded_job_title = urllib.parse.quote(job_title)
    encoded_location = urllib.parse.quote(LOCATION)
    
    search_url = (
        f"https://www.linkedin.com/jobs/search/?keywords={encoded_job_title}"
        f"&location={encoded_location}&f_AL=true&f_WT=2"
    )
    print(f"\n🔍 Searching for: {job_title}")
    print(f"🔗 URL: {search_url}")
    
    driver.get(search_url)
    time.sleep(3)  # Initial wait for page load
    
    if not wait_for_job_cards(driver):
        print(f"⚠️ No job cards found for: {job_title}")
        return []
    
    jobs = get_easy_apply_jobs(driver, max_jobs=MAX_JOBS_PER_TITLE)
    print(f"📊 Found {len(jobs)} Easy Apply jobs for: {job_title}")
    return jobs

def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Optional: run headless
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    driver.get("https://www.linkedin.com")

    input("🔐 Log in to LinkedIn manually, then press Enter to continue...")

    save_cookies(driver)
    load_cookies(driver)
    init_db()

    all_jobs = set()  # Use a set to avoid duplicates
    
    for job_title in JOB_TITLES:
        jobs = search_jobs(driver, job_title)
        all_jobs.update(jobs)
        
        if len(all_jobs) >= MAX_JOBS_PER_TITLE * len(JOB_TITLES):
            print("🎯 Reached maximum job limit")
            break

    print(f"\n📈 Total unique jobs found: {len(all_jobs)}")

    for job_url in all_jobs:
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
