import pandas as pd
import numpy as np

def clean_physical_columns(df, columns):
    """
    Cleans physical columns (e.g., 'height_cm', 'weight_kg') in a DataFrame
    by removing units ('cm', 'kg') and converting to integer type.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        columns (list): A list of column names to clean.

    Returns:
        pd.DataFrame: The DataFrame with cleaned physical columns.
    """
    for col in columns:
        if col not in df.columns:
            print(f"Column '{col}' not found in DataFrame. Skipping.")
            continue

        # Convert column to string to handle various data types, then remove suffixes
        # Use .str accessor to apply string methods, handling potential non-string types
        df[col] = df[col].astype(str).str.replace('cm', '', regex=False)
        df[col] = df[col].astype(str).str.replace('kg', '', regex=False)
        df[col] = df[col].astype(str).str.strip() # Remove any leading/trailing whitespace

        # Convert to numeric, coercing errors to NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')

        # Convert to nullable integer type (Int64Dtype) to allow NaN values
        df[col] = df[col].astype(pd.Int64Dtype())

    return df

if __name__ == '__main__':
    # Create a sample DataFrame to demonstrate the function
    data = {
        'player': ['Player X', 'Player Y', 'Player Z', 'Player W'],
        'height_cm': ['180cm', '175', '190cm', np.nan],
        'weight_kg': ['75kg', '70', '88kg', '65.5kg'] # Demonstrating float parsing
    }
    sample_df = pd.DataFrame(data)
    print("Original DataFrame:")
    print(sample_df)
    print("" + "="*30 + "")

    # The physical columns to be cleaned
    physical_cols = ['height_cm', 'weight_kg']

    # Clean the physical columns
    cleaned_df = clean_physical_columns(sample_df.copy(), physical_cols)
    
    print("Cleaned DataFrame:")
    print(cleaned_df)
    print("" + "="*30 + "")

    # Example with the actual project data
    # Note: The provided 'combined_players_data.csv' already seems to have numeric physical data.
    # This function would be essential if you were loading raw data with string formats like '180cm'.
    try:
        players_df = pd.read_csv('./clean_data/combined_players_data.csv')
        
        # The columns are already numeric, but we can run the function for demonstration
        # It will gracefully handle the numeric data.
        cleaned_players_df = clean_physical_columns(players_df.copy(), physical_cols)
        
        print("First 5 rows of the project DataFrame after applying cleaning function:")
        print(cleaned_players_df[physical_cols].head())
        print(cleaned_players_df[physical_cols].dtypes)

    except FileNotFoundError:
        print("Could not find './clean_data/combined_players_data.csv'.")


