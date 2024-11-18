import json
from typing import List, Dict
import httpx
from parsel import Selector

async def parse_agent_page(response: httpx.Response) -> List[Dict]:
    """Parse the agent listing page and extract agent data."""
    selector = Selector(text=response.text)
    data_text = selector.css("script#__NEXT_DATA__::text").get()
    
    if not data_text:
        print(f"Page {response.url} does not contain agent data")
        return []

    try:
        data = json.loads(data_text)
        props = data.get("props", {})
        page_props = props.get("pageProps", {})
        page_data = page_props.get("pageData", {})
        
        agents_data = page_data.get("agents", [])
        if not isinstance(agents_data, list):
            agents_data = []
        
        print(f"Found {len(agents_data)} agents in pageData")
        
        agents_list = []
        for agent in agents_data:
            # Get served areas safely
            served_areas = []
            try:
                served_areas = [
                    f"{area.get('name')}, {area.get('state_code')}"
                    for area in agent.get("served_areas", [])
                    if area.get('name') and area.get('state_code')
                ]
            except (AttributeError, TypeError):
                pass

            # Get contact information safely
            contact_info = {}
            try:
                phones = agent.get("phones", [])
                if phones:
                    contact_info = {
                        phone.get("type", "Unknown"): phone.get("number")
                        for phone in phones
                        if phone and phone.get("number")
                    }
            except (AttributeError, TypeError):
                pass

            # Get address safely
            address = agent.get("address") or {}
            if not isinstance(address, dict):
                address = {}
            
            # Get brokerage information with specific company name
            brokerage = None
            try:
                # First try to get agent_group as it seems most reliable
                brokerage = agent.get("agent_group")
                if not brokerage:
                    # Fallback options if agent_group is not available
                    brokerage = (
                        agent.get("brokerage_name") or 
                        agent.get("broker", {}).get("name") or 
                        agent.get("broker_name")
                    )
                
                # Clean up any None or empty string values
                if not brokerage:
                    brokerage = None
                    
            except AttributeError:
                brokerage = None

            # Get experience information
            current_year = 2024  # You might want to calculate this dynamically
            first_year = agent.get("first_year", 0)
            years_experience = current_year - first_year if first_year > 0 else 0

            experience = {
                "years": years_experience,
                "active_listings": agent.get("for_sale_count", 0),
                "sold_listings": {
                    "count": agent.get("recently_sold", 0),
                    "min": agent.get("min_price", 0),
                    "max": agent.get("max_price", 0),
                    "last_sold_date": agent.get("last_listing_date")
                },
                "price_range": {
                    "min": agent.get("min_price", 0),
                    "max": agent.get("max_price", 0)
                },
                "last_listing_date": agent.get("last_listing_date")
            }

            agent_info = {
                "name": agent.get("full_name"),
                "brokerage": brokerage,
                "experience": experience,
                "areas_of_business": agent.get("areas_of_business", []),
                "reviews": {
                    "count": agent.get("review_count", 0),
                    "rating": agent.get("agent_rating", 0),
                    "recent_sales": agent.get("recently_sold", 0)  # Updated field name
                },
                "served_areas": served_areas,
                "contact": contact_info,
                "office_address": {
                    "line": address.get("line"),
                    "city": address.get("city"),
                    "state": address.get("state_code"),
                    "zip": address.get("postal_code")
                } if address else None
            }
            agents_list.append(agent_info)

        return agents_list
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return []
