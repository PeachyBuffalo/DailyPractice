import asyncio
import json
from pathlib import Path
from multpage import scrape_agents
from typing import List, Dict
import logging

async def load_config() -> List[Dict]:
    """Load search parameters from config file."""
    config_path = Path(__file__).parent / "config" / "search_params.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    with config_path.open('r', encoding='utf-8') as f:
        content = f.read()
        # Remove comments if present
        content = '\n'.join(line for line in content.split('\n') if '//' not in line)
        return json.loads(content)['searches']
    

async def filter_agents(agents: List[Dict], search_params: Dict) -> List[Dict]:
    """Filter agents based on search parameters."""
    filtered_agents = []
    
    for agent in agents:
        # Extract agent areas
        agent_areas = [area.split(',')[0].strip() for area in agent.get('served_areas', [])]

        # Extract price range from sold listings or fallback to price range
        sold_min = agent['experience']['sold_listings'].get('min', 0)
        sold_max = agent['experience']['sold_listings'].get('max', float('inf'))
        agent_min = sold_min if sold_min > 0 else agent['experience']['price_range'].get('min', 0)
        agent_max = sold_max if sold_max > 0 else agent['experience']['price_range'].get('max', float('inf'))

        # Debug logs to inspect each step
        logging.info(f"Evaluating agent: {agent.get('name', 'Unknown')}")
        logging.info(f"Agent areas: {agent_areas}")
        logging.info(f"Agent sold price range: {sold_min} - {sold_max}")

        # Check area inclusion
        if not any(area in agent_areas for area in search_params['area_specifics']['include_areas']):
            logging.info("Filtered out due to area inclusion mismatch.")
            continue

        # Check area exclusion
        if any(area in agent_areas for area in search_params['area_specifics']['exclude_areas']):
            logging.info("Filtered out due to area exclusion.")
            continue

        # Check budget using adjusted min and max values
        if agent_min > search_params['budget']['max'] or agent_max < search_params['budget']['min']:
            logging.info("Filtered out due to budget mismatch.")
            continue

        # If all conditions pass, add to filtered list
        filtered_agents.append(agent)
        logging.info("Agent added to filtered list.")
    
    logging.info(f"Total filtered agents: {len(filtered_agents)}")
    return filtered_agents


async def main():
    # Load search parameters
    search_params = await load_config()
    
    # Define the output directory
    current_dir = Path(__file__).parent
    output_dir = current_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each search configuration
    for params in search_params:
        print(f"\nProcessing search for {params['city']}, {params['state']}")
        
        # Scrape agents
        agents = await scrape_agents(params['city'], params['state'])
        print(f"Total agents scraped: {len(agents)}")
        
        # Filter agents based on parameters
        filtered_agents = await filter_agents(agents, params)
        print(f"Filtered agents: {len(filtered_agents)}")
        
        # Save filtered results
        output_file = output_dir / f"agents_{params['city']}_{params['state']}_filtered.json"
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(filtered_agents, f, indent=2, ensure_ascii=False)
        
        print(f"Data saved to: {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
