from datetime import datetime, timedelta
import os

def create_daily_folders():
    # Get today's date
    start_date = datetime.now()
    # End of 2024
    end_date = datetime(2024, 12, 31)
    
    # Create a folder for each remaining day
    current_date = start_date
    while current_date <= end_date:
        # Format the year and month-day
        year = current_date.strftime('%Y')
        month_day = current_date.strftime('%b-%d')  # Nov-7 format
        
        # Create the full path
        folder_path = os.path.join(year, month_day)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
            # Create a basic README.md in each folder
            readme_content = f"""# Daily Project - {month_day}, {year}

## Project Title
[Project title goes here]

## Description
[Project description goes here]

## Technologies Used
- [Technology 1]
- [Technology 2]

## Setup Instructions
1. [Setup step 1]
2. [Setup step 2]

## Screenshots
[Add screenshots here]

## Lessons Learned
[What did you learn while building this project?]
"""
            
            # Create README.md
            with open(os.path.join(folder_path, 'README.md'), 'w') as f:
                f.write(readme_content)
            
            # Create Notes.md
            notes_content = """# Project Notes

## Overview
[Project overview goes here]

## Implementation Details
[Technical details go here]

## Challenges Faced
[List challenges and solutions]

## Resources Used
[List helpful resources, tutorials, etc.]

## Future Improvements
[Ideas for future enhancements]
"""
            with open(os.path.join(folder_path, 'Notes.md'), 'w') as f:
                f.write(notes_content)
        
        # Move to next day
        current_date += timedelta(days=1)

if __name__ == "__main__":
    create_daily_folders()
    print("Folders created successfully!")