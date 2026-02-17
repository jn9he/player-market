import pandas as pd
import numpy as np

def clean_financial_columns(df, columns):
    """
    Cleans financial columns in a DataFrame by converting string representations
    (e.g., '€100.5M', '€50K') to numeric values (in euros).

    Args:
        df (pd.DataFrame): The DataFrame to process.
        columns (list): A list of column names to clean.

    Returns:
        pd.DataFrame: The DataFrame with cleaned financial columns.
    """
    for col in columns:
        # Skip if the column does not exist
        if col not in df.columns:
            print(f"Column '{col}' not found in DataFrame. Skipping.")
            continue

        # Convert column to string to handle various data types, handle NaNs
        df[col] = df[col].astype(str).str.strip()

        # Replace 'M' with 6 zeros, 'K' with 3 zeros, and remove currency symbols/commas
        df[col] = df[col].replace({'M': 'e6', 'K': 'e3', '€': ''}, regex=True)
        
        # Convert to numeric, coercing errors to NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


