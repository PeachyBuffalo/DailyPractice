from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import random
import os
from colorama import init, Fore, Style
init()  # Initialize colorama

@dataclass
class Player:
    name: str
    health: int = 100
    inventory: List[str] = None
    current_location: str = "start"
    
    def __post_init__(self):
        self.inventory = self.inventory or []

class GameEngine:
    def __init__(self):
        self.player: Optional[Player] = None
        self.story_data: Dict = self._load_story_data()
        
    def _load_story_data(self) -> Dict:
        try:
            with open("story_data.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{Fore.RED}Error: story_data.json not found!{Style.RESET_ALL}")
            return {}

    def start_game(self):
        print(f"{Fore.CYAN}Welcome to Python Quest!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'=' * 50}{Style.RESET_ALL}")
        
        # Check for saved game
        if os.path.exists("savegame.json"):
            load = input("Saved game found. Would you like to load it? (y/n): ").lower()
            if load == 'y':
                self.load_game()
                return

        name = input("Enter your character's name: ")
        self.player = Player(name=name)
        self.play_scene("start")

    def play_scene(self, scene_id: str):
        if scene_id not in self.story_data:
            print(f"{Fore.RED}Error: Scene '{scene_id}' not found!{Style.RESET_ALL}")
            return

        scene = self.story_data[scene_id]
        
        # Display scene
        print(f"\n{Fore.GREEN}{scene['description']}{Style.RESET_ALL}")
        
        # Random event chance (20%)
        if random.random() < 0.2:
            self.trigger_random_event()

        # Display choices
        if "choices" in scene:
            print("\nWhat would you like to do?")
            for i, choice in enumerate(scene["choices"], 1):
                print(f"{i}. {choice['text']}")
            
            while True:
                try:
                    choice = int(input("\nEnter your choice (or 0 to save game): "))
                    if choice == 0:
                        self.save_game()
                        continue
                    if 1 <= choice <= len(scene["choices"]):
                        next_scene = scene["choices"][choice-1]["next"]
                        self.player.current_location = next_scene
                        self.play_scene(next_scene)
                        break
                    else:
                        print(f"{Fore.YELLOW}Invalid choice. Try again.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.YELLOW}Please enter a number.{Style.RESET_ALL}")
        else:
            print("\nTHE END")

    def trigger_random_event(self):
        events = [
            ("You found a healing potion!", 20),
            ("You stumbled and hurt yourself.", -10),
            ("You found some gold!", 0),
            ("A friendly sprite appears and gives you a blessing.", 15)
        ]
        
        event, health_change = random.choice(events)
        print(f"\n{Fore.MAGENTA}Random Event: {event}{Style.RESET_ALL}")
        
        self.player.health += health_change
        if health_change != 0:
            print(f"Health change: {health_change:+d}")
            print(f"Current health: {self.player.health}")

    def save_game(self):
        save_data = {
            "name": self.player.name,
            "health": self.player.health,
            "inventory": self.player.inventory,
            "current_location": self.player.current_location
        }
        
        with open("savegame.json", "w") as f:
            json.dump(save_data, f)
        print(f"{Fore.GREEN}Game saved successfully!{Style.RESET_ALL}")

    def load_game(self):
        try:
            with open("savegame.json", "r") as f:
                save_data = json.load(f)
                self.player = Player(
                    name=save_data["name"],
                    health=save_data["health"],
                    inventory=save_data["inventory"],
                    current_location=save_data["current_location"]
                )
            print(f"{Fore.GREEN}Game loaded successfully!{Style.RESET_ALL}")
            self.play_scene(self.player.current_location)
        except FileNotFoundError:
            print(f"{Fore.RED}No saved game found!{Style.RESET_ALL}")

if __name__ == "__main__":
    game = GameEngine()
    game.start_game()