import pandas as pd
import numpy as np

def remove_goalkeepers(df):
    """
    Removes goalkeeper entries from the DataFrame based on the 'player_positions' column.

    Args:
        df (pd.DataFrame): The input DataFrame containing player data.

    Returns:
        pd.DataFrame: A new DataFrame with goalkeeper entries removed.
    """
    initial_rows = len(df)
    
    # Identify rows where 'player_positions' contains 'GK'
    # We use .str.contains() with regex=False for simple substring matching
    # and case=False to handle potential 'gk' or 'GK' variations
    # na=False ensures that NaN values in 'player_positions' do not raise an error
    goalkeeper_mask = df['player_positions'].str.contains('GK', na=False, case=False)
    
    # Filter out goalkeepers
    field_players_df = df[~goalkeeper_mask].copy()
    
    removed_rows = initial_rows - len(field_players_df)
    
    print(f"Successfully identified and removed {removed_rows} goalkeeper entries.")
    print(f"DataFrame shape before removal: {df.shape}")
    print(f"DataFrame shape after removal: {field_players_df.shape}")
    
    return field_players_df

if __name__ == '__main__':
    file_path = './clean_data/combined_players_data.csv'

    try:
        # Load the dataset
        df = pd.read_csv(file_path, low_memory=False)
        print(f"Successfully loaded '{file_path}'")

        print("--- Original DataFrame Info ---")
        print(f"Number of rows: {len(df)}")
        # Check initial distribution of GKs
        print("Initial player_positions counts (top 5):")
        print(df['player_positions'].value_counts().head())

        # Remove goalkeepers
        df_field_players = remove_goalkeepers(df.copy()) # Use a copy to not modify original df

        print("--- DataFrame After Goalkeeper Removal ---")
        print(f"Number of rows: {len(df_field_players)}")
        # Verify that 'GK' is no longer a primary position
        print("Player_positions counts after removal (top 5):")
        print(df_field_players['player_positions'].value_counts().head())

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please ensure the path is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")
