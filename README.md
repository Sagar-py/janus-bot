# Janus Bot 🤖 – LinkedIn Easy Apply Automation

Janus Bot is a Python-based automation tool designed to streamline job applications on LinkedIn by targeting "Easy Apply" job listings. It leverages Selenium to simulate browser interactions, helping you apply to multiple jobs with minimal effort.

## Features

- Automatically logs in using saved cookies
- Searches for jobs matching your role and location
- Filters for LinkedIn's "Easy Apply" listings
- Applies using a pre-uploaded resume
- Tracks applications to avoid duplicates
- Uses a local SQLite database to store job URLs

## Requirements

- Python 3.8+
- Google Chrome browser
- ChromeDriver installed and accessible in your PATH
- A LinkedIn account

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Configuration
Edit the `config.py` file:
```python
JOB_TITLE = "Machine Learning Engineer"
LOCATION = "India"
RESUME_PATH = "/absolute/path/to/your/resume.pdf"
```

## Usage
1. Login manually to LinkedIn: The bot will open LinkedIn in Chrome. Log in yourself — this is required for authentication.
2. Start the bot:
```bash
python main.py
```
3. What happens next:
   - Bot will navigate to the job search page
   - Scrape "Easy Apply" job URLs
   - Attempt to apply to each job
   - Log each attempt in `applied_jobs.db`

## Project Structure
```bash
janus-bot/
├── apply_handler.py      # Handles the application process
├── config.py             # Stores job title, location, resume path
├── job_scraper.py        # Extracts Easy Apply job URLs
├── main.py               # Main driver script
├── utils.py              # Cookie handling, DB tracking
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Troubleshooting
- ❌ "Found 0 Easy Apply jobs"
Double-check your JOB_TITLE/LOCATION and loosen filters. Make sure LinkedIn isn't blocking access or showing the login wall again.
- ❌ TimeoutException on job cards
LinkedIn may have changed its HTML structure. Update CSS selectors in job_scraper.py.
- ❌ SessionNotCreatedException (Safari)
If using Safari, make sure "Allow Remote Automation" is enabled. Chrome is recommended.

## Disclaimer
This project is intended for educational and personal use only. Automating LinkedIn interactions may violate their Terms of Service. Use responsibly.