from typing import List, Dict
import httpx
from agentdatascrape import parse_agent_page

async def scrape_agents(city: str, state: str) -> List[Dict]:
    """Scrape agent data for a specific city and state."""
    agents = []
    page = 1
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as session:
        while True:
            url = f"https://www.realtor.com/realestateagents/{city}_{state}/pg-{page}"
            print(f"Attempting to fetch URL: {url}")
            response = await session.get(url)
            print(f"Response status: {response.status_code}")
            print(f"Response text preview: {response.text[:200]}")
            
            if response.status_code != 200:
                print(f"Failed to retrieve page {page} (status code: {response.status_code})")
                break

            page_agents = await parse_agent_page(response)
            if not page_agents:
                print(f"No agents found on page {page}. Ending scrape.")
                break

            agents.extend(page_agents)
            print(f"Scraped page {page} with {len(page_agents)} agents.")
            page += 1

    return agents