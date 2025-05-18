import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def apply_to_job(driver, job_url, resume_path):
    driver.get(job_url)
    time.sleep(3)  # Wait for the page to load
    try:
        apply_button = driver.find_element(By.CLASS_NAME, "jobs-apply-button")
        apply_button.click()
        time.sleep(2)  # Wait for the application to open

        # Upload resume
        upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        upload_input.send_keys(resume_path)
        time.sleep(2)  # Wait for the file to upload

        # Submit application
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']")
        submit_button.click()
        time.sleep(2)  # Wait for the application to submit

        return True
    except NoSuchElementException:
        return False