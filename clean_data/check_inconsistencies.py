import pandas as pd
import numpy as np

def check_dataframe_inconsistencies(df):
    """
    Scans through each column of a DataFrame and lists potential inconsistencies,
    including NaN values, data types, and unique values for non-numeric columns.

    Args:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        None: Prints the inconsistencies directly.
    """
    print("--- Checking DataFrame for General Inconsistencies ---")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}\n")

    for col in df.columns:
        print(f"--- Column: '{col}' ---")
        
        nan_count = df[col].isnull().sum()
        if nan_count > 0:
            nan_percentage = (nan_count / len(df)) * 100
            print(f"  - Missing Values (NaN): {nan_count} ({nan_percentage:.2f}%)")
        else:
            print("  - No Missing Values (NaN)")

        dtype = df[col].dtype
        print(f"  - Data Type: {dtype}")

        if dtype == 'object' or isinstance(df[col].dtype, pd.CategoricalDtype):
            unique_values = df[col].nunique()
            if unique_values < 20 and unique_values > 0:
                print(f"  - Unique Values ({unique_values}):")
                print(df[col].value_counts(dropna=False))
            elif unique_values > 20:
                print(f"  - Unique Values: {unique_values} (too many to list, showing top 5)")
                print(df[col].value_counts(dropna=False).head())
            else:
                print("  - No unique non-NaN values.")
        
        elif pd.api.types.is_numeric_dtype(df[col]):
            if nan_count == 0:
                print(f"  - Min: {df[col].min()}, Max: {df[col].max()}")
            else:
                print(f"  - Min (non-NaN): {df[col].min()}, Max (non-NaN): {df[col].max()}")
        
        print("-" * (len(col) + 14) + "\n")

def check_special_inconsistencies(df):
    """
    Checks for specific inconsistencies like duplicate names and logical errors.

    Args:
        df (pd.DataFrame): The DataFrame to check.
    """
    print("--- Checking for Special Inconsistencies (Duplicates and Logic) ---")

    # 1. Check for duplicate player names
    for name_col in ['short_name', 'long_name']:
        if name_col in df.columns:
            duplicates = df[name_col].value_counts()
            duplicates = duplicates[duplicates > 1]
            if not duplicates.empty:
                print(f"\n--- Duplicate '{name_col}' Found ---")
                print(f"  - Total unique names with duplicates: {len(duplicates)}")
                print("  - Most frequent duplicates:")
                print(duplicates.head())
            else:
                print(f"\n--- No Duplicates Found in '{name_col}' ---")

    # 2. Check for more specific duplicates (same name, birthday, and nationality)
    # These are very likely to be true data entry errors.
    id_cols = ['long_name', 'dob', 'nationality_name']
    if all(col in df.columns for col in id_cols):
        specific_duplicates = df.duplicated(subset=id_cols, keep=False)
        if specific_duplicates.any():
            print("\n--- Highly Likely Duplicate Player Entries Found ---")
            print("Based on same long_name, dob, and nationality_name.")
            print(df[specific_duplicates].sort_values(by=id_cols))
        else:
            print("\n--- No highly likely duplicate entries found ---")
            
    # 3. Check for logical inconsistencies in age
    if 'age' in df.columns:
        print("\n--- Checking for Age Inconsistencies ---")
        unrealistic_age = df[(df['age'] < 15) | (df['age'] > 50)]
        if not unrealistic_age.empty:
            print("  - Found players with potentially unrealistic ages (<15 or >50):")
            print(unrealistic_age[['short_name', 'age']])
        else:
            print("  - No players with unrealistic ages found.")
            
    print("\n--- Special Inconsistency Check Finished ---\n")


if __name__ == '__main__':
    # Path to the dataset
    file_path = './clean_data/combined_players_data.csv'

    try:
        # Load the dataset with low_memory=False to avoid mixed type errors
        df = pd.read_csv(file_path, low_memory=False)
        print(f"Successfully loaded '{file_path}'\n")

        # Perform the general inconsistency check
        check_dataframe_inconsistencies(df)
        
        # Perform the special inconsistency check for duplicates and logic errors
        check_special_inconsistencies(df)

    except FileNotFoundError:
        print(f"Error: The file '{file_p}' was not found. Please ensure the path is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")
