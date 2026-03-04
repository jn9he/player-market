import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create a directory to save the plots
if not os.path.exists('plots'):
    os.makedirs('plots')

# Load the dataset
file_path = 'clean_data/cleaned_csvs/timeseries_fifa_players.csv'
df = pd.read_csv(file_path)

# Group by year and player_positions and calculate the mean overall rating
avg_rating_by_pos_year = df.groupby(['year', 'player_positions'])['overall'].mean().reset_index()

# Get unique years
years = avg_rating_by_pos_year['year'].unique()

# Create a plot for each year
for year in years:
    plt.figure(figsize=(12, 8))
    year_data = avg_rating_by_pos_year[avg_rating_by_pos_year['year'] == year]
    
    # Sort data for better visualization
    sorted_data = year_data.sort_values(by='overall', ascending=False)
    
    sns.barplot(x='overall', y='player_positions', data=sorted_data, orient='h')
    
    plt.title(f'Average Player Rating by Position in {year}')
    plt.xlabel('Average Overall Rating')
    plt.ylabel('Player Position')
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(f'plots/average_rating_by_position_{year}.png')
    plt.close()

print("Histograms created and saved as PNG files in the 'plots' directory.")
