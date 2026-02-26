def combine_fifa_datasets(base_path="FIFA_PLAYERDATA", output_filename="combined_players_data.csv"):
    """
    Combines FIFA player datasets from players_15.csv to players_22.csv into a single DataFrame.
    Saves the combined DataFrame to a new CSV file.
    """
    all_data = []
    
    print(f"Combining datasets from {base_path}...")

    for year in range(15, 23):  # Includes 15 to 22
        filename = f"players_{year}.csv"
        filepath = os.path.join(base_path, filename)
        
        if os.path.exists(filepath):
            print(f"Reading {filename}...")
            try:
                df = pd.read_csv(filepath)
                all_data.append(df)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        else:
            print(f"File not found: {filename}")
            
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"Successfully combined {len(all_data)} datasets. Total rows: {len(combined_df)}")
        
        output_filepath = os.path.join(os.getcwd(), output_filename)
        combined_df.to_csv(output_filepath, index=False)
        print(f"Combined data saved to {output_filepath}")
    else:
        print("No data was combined.")

if __name__ == "__main__":
    combine_fifa_datasets()
