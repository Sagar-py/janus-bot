import pickle
import sqlite3

def save_cookies(driver, path="cookies.pkl"):
    with open(path, "wb") as f:
        pickle.dump(driver.get_cookies(), f)

def load_cookies(driver, path="cookies.pkl"):
    import os
    if not os.path.exists(path):
        return
    driver.get("https://www.linkedin.com")
    with open(path, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

def init_db():
    conn = sqlite3.connect("applied_jobs.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS applied_jobs (url TEXT PRIMARY KEY)")
    conn.commit()
    conn.close()

def mark_applied(job_url):
    conn = sqlite3.connect("applied_jobs.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO applied_jobs (url) VALUES (?)", (url,))
    conn.commit()
    conn.close()

def already_applied(url):
    conn = sqlite3.connect("applied_jobs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM applied_jobs WHERE url=?", (url,))
    result = c.fetchone()
    conn.close()
    return result is not None

