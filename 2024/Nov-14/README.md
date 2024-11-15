# Daily Project - Nov-14, 2024

## Project Title
Real Estate Agent Search API expansion of Nov-12 project

## Description
A Flask-based API system that provides access to pre-scraped real estate agent data. The application combines web scraping capabilities with a REST API to deliver filtered agent information based on location parameters.

## Technologies Used
- Python 3.x
- Flask
- Gunicorn
- Web Scraping Tools
  - Beautiful Soup/Parsel
  - Requests/HTTPX
- JSON for data storage
- Shell scripting

## Setup Instructions
1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the scraper to populate data:
   ```bash
   python runsearch.py
   ```
5. Start the API server:
   ```bash
   ./start.sh
   ```

## Screenshots
[To be added: API endpoint responses, data structure examples]

## Lessons Learned
- Importance of separating data collection from API serving
- Benefits of pre-processing data vs. real-time scraping
- Challenges in maintaining data freshness
- Best practices for API endpoint design
- Efficient JSON file handling for data storage
