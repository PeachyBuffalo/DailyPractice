import asyncio
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from typing_extensions import TypedDict

import httpx
from parsel import Selector

...  # NOTE: include code from property scraping section

async def scrape_feed(url) -> Dict[str, datetime]:
    """scrapes atom RSS feed and returns all entries in "url:publish date" format"""
    response = await session.get(url)
    selector = Selector(text=response.text, type="xml")
    results = {}
    for item in selector.xpath("//item"):
        url = item.xpath("link/text()").get()
        pub_date = item.xpath("pubDate/text()").get()
        results[url] = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S")
    return results


async def track_feed(url: str, output: Path, interval: int = 60):
    """Track Realtor.com feed, scrape new listings and append them as JSON to the output file"""
    # to prevent duplicates let's keep a set of property IDs we already scraped
    seen = set()
    output.touch(exist_ok=True)  # create file if it doesn't exist
    try:
        while True:
            # scrape feed for listings
            listings = await scrape_feed(url=url)
            # remove listings we scraped in previous loops
            listings = {k: v for k, v in listings.items() if f"{k}:{v}" not in seen}
            if listings:
                # scrape properties and save to file - 1 property as JSON per line
                properties = await scrape_properties(list(listings.keys()))
                with output.open("a") as f:
                    f.write("\n".join(json.dumps(property) for property in properties))

                # add seen to deduplication filter
                for k, v in listings.items():
                    seen.add(f"{k}:{v}")
            print(f"scraped {len(properties)} properties; waiting {interval} seconds")
            await asyncio.sleep(interval)
    except KeyboardInterrupt:  # Note: CTRL+C will gracefully stop our scraper
        print("stopping price tracking")