import asyncio
import json
from typing import List, Dict

import httpx
from parsel import Selector

# Set up HTTPX client with headers
BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;"
              "q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
}
session = httpx.AsyncClient(headers=BASE_HEADERS, follow_redirects=True)
