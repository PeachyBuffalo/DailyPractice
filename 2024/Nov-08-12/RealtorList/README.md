# Daily Project - Nov-12, 2024

## Project Title
Realtor.com Agent Scraper

## Description
An asynchronous web scraper built in Python that extracts real estate agent information from Realtor.com. The scraper collects agent names, business areas, review counts, served areas, and contact information for a specified city and state.

## Technologies Used
- Python 3.12
- httpx (async HTTP client)
- parsel (HTML/XML parsing)
- asyncio (asynchronous I/O)
- pathlib (file path handling)
- JSON (data storage)

## Setup Instructions
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install httpx parsel
   ```

3. Run the scraper:
   ```bash
   python runsearch.py
   ```

## Project Structure
RealtorList/
├── agent

## Screenshots
[Add screenshots here]

## Lessons Learned
1. Asynchronous Programming
   - Efficient handling of multiple HTTP requests
   - Error handling in async context

2. Data Parsing
   - Safe navigation of nested JSON structures
   - Handling missing or malformed data

3. Error Handling
   - Implementing robust error checking
   - Graceful handling of missing fields

4. File Organization
   - Structured project layout
   - Modular code design

5. Data Storage
   - JSON file handling
   - Proper encoding and formatting
