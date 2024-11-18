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
    # Add debug prints
    print("\nFilter Parameters:")
    print(f"Include Areas: {search_params['area_specifics']['include_areas']}")
    print(f"Exclude Areas: {search_params['area_specifics']['exclude_areas']}")
    print(f"Budget Range: ${search_params['budget']['min']:,} - ${search_params['budget']['max']:,}")
    
    filtered_agents = []
    
    for agent in agents:
        # Extract agent areas - Update this to be case-insensitive
        agent_areas = [area.split(',')[0].strip().lower() for area in agent.get('served_areas', [])]
        search_include_areas = [area.lower() for area in search_params['area_specifics']['include_areas']]
        search_exclude_areas = [area.lower() for area in search_params['area_specifics']['exclude_areas']]

        # Debug print for first few agents
        if len(filtered_agents) == 0:
            print(f"\nExample Agent:")
            print(f"Name: {agent.get('name')}")
            print(f"Areas: {agent.get('served_areas')}")
            print(f"Price Range: {agent['experience']['sold_listings'].get('min')} - {agent['experience']['sold_listings'].get('max')}")

        # Extract price range from sold listings count instead of direct min/max
        sold_listings = agent['experience']['sold_listings'].get('count', {})
        agent_min = sold_listings.get('min', 0)
        agent_max = sold_listings.get('max', float('inf'))

        # Check area inclusion - Update logic
        if not any(include_area in agent_areas for include_area in search_include_areas):
            continue

        # Check area exclusion
        if any(exclude_area in agent_areas for exclude_area in search_exclude_areas):
            continue

        # Check budget using adjusted min and max values
        if (agent_min > search_params['budget']['max'] or 
            agent_max < search_params['budget']['min']):
            continue

        # If all conditions pass, add to filtered list
        filtered_agents.append(agent)
    
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
