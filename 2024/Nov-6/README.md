# Daily Project - Nov-6, 2024

## Project Title
Personal Finance Tracker CLI

## Description
A command-line interface (CLI) application built in Python that helps users track and visualize their daily expenses. The application stores expense data persistently using JSON and provides visual analytics through matplotlib pie charts.

## Technologies Used
- Python 3.x
- matplotlib for data visualization
- JSON for data persistence
- datetime for timestamp handling
- pathlib for file path management

## Setup Instructions
1. Ensure Python 3.x is installed on your system
2. Install required dependencies:
   ```
   pip install matplotlib
   ```
3. Navigate to the project directory:
   ```
   cd 2024/Nov-6
   ```
4. Run the application:
   ```
   python finance_tracker.py
   ```

## Screenshots
[To be added after running the application]

## Lessons Learned
1. **Object-Oriented Design**
   - Implemented a FinanceTracker class to encapsulate expense management logic
   - Used class methods for data loading and saving operations

2. **Data Persistence**
   - Utilized JSON for storing expense data between sessions
   - Implemented error handling for file operations

3. **Data Visualization**
   - Created pie charts using matplotlib for expense category analysis
   - Learned to format and display financial data effectively

4. **User Interface Design**
   - Developed a simple but effective command-line menu system
   - Implemented input validation and user feedback

5. **File I/O Operations**
   - Managed file reading and writing operations
   - Handled FileNotFoundError exceptions gracefully

6. **Data Structure Management**
   - Used dictionaries for category-based expense tracking
   - Implemented list operations for expense storage
