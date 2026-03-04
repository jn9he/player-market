
import pandas as pd

def filter_players_by_year(input_path, output_path):
    # First pass: count player occurrences
    player_counts = pd.Series(dtype=int)
    chunk_iter = pd.read_csv(input_path, chunksize=100000, low_memory=False)
    for chunk in chunk_iter:
        player_counts = player_counts.add(chunk['short_name'].value_counts(), fill_value=0)

    # Identify players with complete records (8 years)
    complete_players = player_counts[player_counts == 8].index

    # Second pass: filter and write to new CSV
    first_chunk = True
    chunk_iter = pd.read_csv(input_path, chunksize=100000, low_memory=False)
    for chunk in chunk_iter:
        filtered_chunk = chunk[chunk['short_name'].isin(complete_players)]
        if first_chunk:
            filtered_chunk.to_csv(output_path, index=False, mode='w')
            first_chunk = False
        else:
            filtered_chunk.to_csv(output_path, index=False, mode='a', header=False)

if __name__ == "__main__":
    input_file = 'clean_data/cleaned_csvs/timeseries_fifa_players.csv'
    output_file = 'clean_data/cleaned_csvs/filtered_timeseries_fifa_players.csv'
    filter_players_by_year(input_file, output_file)
    print(f"Filtered data saved to {output_file}")
