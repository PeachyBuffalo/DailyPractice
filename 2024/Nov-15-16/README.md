# Daily Project - Nov-15, 2024

## Project Title
Python Quest: A Text Adventure Engine

## Description
An interactive text-based adventure game that demonstrates Python's capabilities in creating engaging, narrative experiences. The game features:
- Multiple story paths with different endings
- Random events system with health management
- Save/Load game functionality
- Colored terminal output for better user experience
- JSON-based story structure for easy content management

## Technologies Used
- Python 3.10+
- colorama (for colored terminal output)
- json (for story and save game handling)
- typing (for type hints)
- random (for event generation)
- dataclasses (for structured data management)

## Setup Instructions
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - Windows: 
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS: 
     ```bash
     source venv/bin/activate
     ```
3. Install requirements:
   ```bash
   pip install colorama
   ```
4. Ensure both `adventure_game.py` and `story_data.json` are in the same directory
5. Run the game:
   ```bash
   python adventure_game.py
   ```

## Game Features
- **Multiple Endings**: Discover different conclusions based on your choices
- **Random Events**: Experience unexpected encounters that affect your health
- **Save System**: Save your progress at any time by entering '0'
- **Health System**: Manage your character's health through various events
- **Colored Interface**: Enjoy a visually enhanced terminal experience
- **Error Handling**: Robust error handling for file operations and user input

## Code Structure
- `adventure_game.py`: Main game engine and logic
- `story_data.json`: Story content and game flow structure
- Key classes:
  - `Player`: Manages player state and inventory
  - `GameEngine`: Handles game mechanics and flow

## Screenshots
[Screenshots showing:
- Game start and character creation
- Colored text output in action
- Random event occurrence
- Multiple choice navigation
- Save/load system interface]

## Lessons Learned
- Implementing object-oriented design patterns in Python
- Managing game state and persistence using JSON
- Creating an engaging user interface in a terminal environment
- Structuring a larger Python project with multiple components
- Using type hints for better code maintainability
- Handling user input and error cases gracefully
- Organizing game content separately from game logic

## Future Improvements
- Add sound effects and background music using pygame
- Implement a more complex inventory system
- Create a GUI version using tkinter
- Add more story branches and random events
- Implement an achievement system
- Add character classes with different abilities
- Create a level system with experience points
