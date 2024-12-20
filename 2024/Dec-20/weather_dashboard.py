import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("800x600")
        
        # Load API key from .env file
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Search section
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.grid(row=0, column=0, pady=10)
        
        self.location_var = tk.StringVar(value="London")
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.location_var, width=30)
        self.search_entry.grid(row=0, column=0, padx=5)
        
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.fetch_weather)
        self.search_button.grid(row=0, column=1)
        
        # Weather display section
        self.weather_frame = ttk.LabelFrame(self.main_frame, text="Current Weather", padding="10")
        self.weather_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        
        self.temp_label = ttk.Label(self.weather_frame, text="Temperature: --")
        self.temp_label.grid(row=0, column=0, pady=5)
        
        self.condition_label = ttk.Label(self.weather_frame, text="Condition: --")
        self.condition_label.grid(row=1, column=0, pady=5)
        
        self.humidity_label = ttk.Label(self.weather_frame, text="Humidity: --")
        self.humidity_label.grid(row=2, column=0, pady=5)
        
        # Initial weather fetch
        self.fetch_weather()

    def fetch_weather(self):
        try:
            params = {
                'q': self.location_var.get(),
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            weather_data = response.json()
            
            # Update display
            self.temp_label.config(text=f"Temperature: {weather_data['main']['temp']}°C")
            self.condition_label.config(text=f"Condition: {weather_data['weather'][0]['description'].title()}")
            self.humidity_label.config(text=f"Humidity: {weather_data['main']['humidity']}%")
            
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")
        except KeyError as e:
            messagebox.showerror("Error", "Invalid data received from weather service")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main() 