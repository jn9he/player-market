
import pandas as pd
import os

def create_timeseries_dataset():
    """
    Combines cleaned FIFA player datasets from different years into a single time-series dataset.

    - Reads all 'players_XX.csv' files from the 'clean_data/cleaned_csvs/' directory.
    - Extracts the year from each filename and adds it as a 'year' column.
    - Concatenates the dataframes.
    - Saves the combined dataset to 'clean_data/cleaned_csvs/timeseries_fifa_players.csv'.
    """
    input_dir = 'clean_data/cleaned_csvs/'
    output_file = os.path.join(input_dir, 'timeseries_fifa_players.csv')
    
    csv_files = [f for f in os.listdir(input_dir) if f.startswith('players_') and f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return

    all_dfs = []
    for file in sorted(csv_files):
        year_str = file.split('_')[1].split('.')[0]
        year = int(f"20{year_str}")
        
        file_path = os.path.join(input_dir, file)
        df = pd.read_csv(file_path)
        df['year'] = year
        all_dfs.append(df)
        print(f"Processed {file} for year {year}")

    if not all_dfs:
        print("No dataframes to combine.")
        return

    combined_df = pd.concat(all_dfs, ignore_index=True)

    # To handle player name 'repeats' across years, we can create a unique identifier
    # for each player-year combination. The user's request is a bit ambiguous,
    # but 'long_name' and 'year' should suffice to identify a player in a given year.
    # If a more specific ID is needed, this is where it would be created.
    # For now, the 'year' column serves as the time-series identifier.

    combined_df.to_csv(output_file, index=False)
    print(f"Combined dataset saved to {output_file}")
    print(f"Total players in combined dataset: {len(combined_df)}")
    print("Columns in combined dataset:", combined_df.columns.tolist())


if __name__ == '__main__':
    create_timeseries_dataset()
