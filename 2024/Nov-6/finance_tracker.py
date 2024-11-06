import datetime
import json
import matplotlib.pyplot as plt
from pathlib import Path

class FinanceTracker:
    def __init__(self):
        self.data_file = "expenses.json"
        self.expenses = self._load_expenses()
        
    def _load_expenses(self):
        """Load existing expenses from JSON file"""
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
            
    def add_expense(self, amount: float, category: str, description: str = ""):
        """Add a new expense"""
        expense = {
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'amount': amount,
            'category': category,
            'description': description
        }
        self.expenses.append(expense)
        self._save_expenses()
        
    def _save_expenses(self):
        """Save expenses to JSON file"""
        with open(self.data_file, 'w') as file:
            json.dump(self.expenses, file, indent=4)
            
    def get_total_expenses(self):
        """Calculate total expenses"""
        return sum(expense['amount'] for expense in self.expenses)
    
    def get_expenses_by_category(self):
        """Get expenses grouped by category"""
        categories = {}
        for expense in self.expenses:
            category = expense['category']
            categories[category] = categories.get(category, 0) + expense['amount']
        return categories
    
    def visualize_expenses(self):
        """Create a pie chart of expenses by category"""
        categories = self.get_expenses_by_category()
        
        plt.figure(figsize=(10, 8))
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title('Expenses by Category')
        plt.axis('equal')
        plt.show()

def main():
    tracker = FinanceTracker()
    
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Expense")
        print("2. View Total Expenses")
        print("3. View Expenses by Category")
        print("4. Visualize Expenses")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            amount = float(input("Enter amount: "))
            category = input("Enter category (food, transport, utilities, etc.): ")
            description = input("Enter description (optional): ")
            tracker.add_expense(amount, category, description)
            print("Expense added successfully!")
            
        elif choice == '2':
            total = tracker.get_total_expenses()
            print(f"\nTotal Expenses: ${total:.2f}")
            
        elif choice == '3':
            categories = tracker.get_expenses_by_category()
            print("\nExpenses by Category:")
            for category, amount in categories.items():
                print(f"{category}: ${amount:.2f}")
                
        elif choice == '4':
            tracker.visualize_expenses()
            
        elif choice == '5':
            print("Thank you for using Personal Finance Tracker!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 