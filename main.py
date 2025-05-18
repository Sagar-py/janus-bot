# This script uses Selenium to open LinkedIn in a Chrome browser
from selenium import webdriver

def main():
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com")
    input("Press Enter to quit")
    driver.quit()

if __name__ == "__main__":
    main()