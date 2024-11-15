import asyncio
import json
import math
from typing import List, Optional

import httpx
from parsel import Selector
from typing_extensions import TypedDict

# 1. Establish persisten HTTPX session with browser-like headers to avoid blocking
BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}
session = httpx.AsyncClient(headers=BASE_HEADERS, follow_redirects=True)

...

# Type hints for search results
# note: the property preview contains a lot of data though not the whole dataset
class PropertyPreviewResult(TypedDict):
    property_id: str
    listing_id: str
    permalink: str
    list_price: int
    price_reduces_amount: Optional[int]
    description: dict
    location: dict
    photos: List[dict]
    list_date: str
    last_update_date: str
    tags: List[str]
    ...  # and more

# Type hint for search results of a single page
class SearchResults(TypedDict):
    count: int  # results on this page
    total: int  # total results for all pages
    results: List[PropertyPreviewResult]


def parse_search(response: httpx.Response) -> SearchResults:
    """Parse Realtor.com search for hidden search result data"""
    selector = Selector(text=response.text)
    data = selector.css("script#__NEXT_DATA__::text").get()
    if not data:
        print(f"page {response.url} is not a property listing page")
        return
    data = json.loads(data)["props"]["pageProps"]
    if not data.get('properties'):  # a|b testing, sometimes it's in a different location
        data['properties'] = data["searchResults"]["home_search"]["results"]
    if not data.get('totalProperties'):
        data['totalProperties'] = data['searchResults']['home_search']['total']
    return data


async def find_properties(state: str, city: str):
    """Scrape Realtor.com search for property preview data"""
    print(f"scraping first result page for {city}, {state}")
    first_page = f"https://www.realtor.com/realestateandhomes-search/{city}_{state.upper()}/pg-1"
    first_result = await session.get(first_page)
    first_data = parse_search(first_result)
    results = first_data["properties"]
    total_pages = math.ceil(first_data["totalProperties"] / len(results))
    print(f"found {total_pages} total pages")

    to_scrape = []
    for page in range(1, total_pages + 1):
        assert "pg-1" in str(first_result.url)  # make sure we don't accidently scrape duplicate pages
        page_url = str(first_result.url).replace("pg-1", f"pg-{page}")
        to_scrape.append(session.get(page_url))
    for response in asyncio.as_completed(to_scrape):
        parsed = parse_search(await response)
        results.extend(parsed["properties"])
    print(f"scraped search of {len(results)} results for {city}, {state}")
    return results