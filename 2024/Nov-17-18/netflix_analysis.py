import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class NetflixAnalyzer:
    def __init__(self, file_path='ViewingActivity.csv'):
        """Initialize the Netflix data analyzer."""
        print("Loading Netflix viewing history...")
        self.df = self.load_and_clean_data(file_path)
        
    def load_and_clean_data(self, file_path):
        """Load and clean the Netflix viewing data."""
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Convert Start Time to datetime with UTC timezone
            df['Start Time'] = pd.to_datetime(df['Start Time'], utc=True)
            
            # Convert to local timezone (US/Eastern)
            df = df.set_index('Start Time')
            df.index = df.index.tz_convert('US/Eastern')
            df = df.reset_index()
            
            # Convert Duration to timedelta
            df['Duration'] = pd.to_timedelta(df['Duration'])
            
            return df
            
        except FileNotFoundError:
            print(f"Error: Could not find {file_path}")
            return None

    def analyze_show(self, show_name="The Office (U.S.)", min_duration='0 days 00:01:00'):
        """Analyze viewing patterns for a specific show."""
        if self.df is None:
            return
        
        # Filter for the specific show
        show_df = self.df[self.df['Title'].str.contains(show_name, regex=False)]
        
        # Filter out very short durations (like previews)
        show_df = show_df[show_df['Duration'] > pd.Timedelta(min_duration)]
        
        # Add weekday and hour columns
        show_df['weekday'] = show_df['Start Time'].dt.weekday
        show_df['hour'] = show_df['Start Time'].dt.hour
        
        # Calculate total watch time
        total_time = show_df['Duration'].sum()
        
        print(f"\n=== {show_name} Viewing Statistics ===")
        print(f"Total time spent watching: {total_time}")
        print(f"Number of episodes watched: {len(show_df)}")
        
        return show_df

    def plot_viewing_patterns(self, show_df):
        """Create visualizations of viewing patterns."""
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        matplotlib.rcParams.update({'font.size': 12})
        
        # Create a figure with multiple subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
        
        # Plot 1: Episodes by Day of Week
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                'Friday', 'Saturday', 'Sunday']
        by_day = show_df['weekday'].value_counts().sort_index()
        by_day.index = [days[i] for i in by_day.index]
        by_day.plot(kind='bar', ax=ax1)
        ax1.set_title('Episodes Watched by Day of Week')
        ax1.set_ylabel('Number of Episodes')
        
        # Plot 2: Episodes by Hour
        by_hour = show_df['hour'].value_counts().sort_index()
        by_hour.plot(kind='bar', ax=ax2)
        ax2.set_title('Episodes Watched by Hour of Day')
        ax2.set_xlabel('Hour (24-hour format)')
        ax2.set_ylabel('Number of Episodes')
        
        plt.tight_layout()
        plt.savefig('viewing_patterns.png')
        plt.close()

def main():
    """Main function to run the Netflix viewing analysis."""
    print("Netflix Viewing History Analysis")
    print("===============================")
    
    # Initialize analyzer
    analyzer = NetflixAnalyzer()
    
    # Analyze The Office
    office_df = analyzer.analyze_show()
    
    if office_df is not None:
        # Create visualizations
        print("\nGenerating viewing pattern visualizations...")
        analyzer.plot_viewing_patterns(office_df)
        print("\nAnalysis complete! Check 'viewing_patterns.png' for visualizations.")

if __name__ == "__main__":
    main() 