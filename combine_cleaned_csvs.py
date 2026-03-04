import pandas as pd
import os
import re

# Define the input and output directories
input_dir = '/Users/joshnghe/Desktop/csu/spring2026/stat472/group-project/player-market/clean_data/cleaned_csvs'
output_file = '/Users/joshnghe/Desktop/csu/spring2026/stat472/group-project/player-market/clean_data/cleaned_csvs/timeseries_fifa_players.csv'

# Get a list of all CSV files in the input directory that match the player data pattern
all_files = os.listdir(input_dir)
player_files = sorted([f for f in all_files if re.match(r'players_\d+\.csv', f)])

# Initialize an empty list to store DataFrames
dfs = []

# Loop through each player CSV file
for file in player_files:
    # Construct the full file path
    file_path = os.path.join(input_dir, file)
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Extract the year from the file name
    year_suffix = re.search(r'(\d+)', file).group(1)
    
    # Add a 'year' column to the DataFrame
    df['year'] = f"20{year_suffix}"
    
    # Append the DataFrame to the list
    dfs.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined data saved to {output_file}")
else:
    print("No player CSV files found to combine.")
