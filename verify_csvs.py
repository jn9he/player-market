import pandas as pd
import os

def verify_csv_schemas(directory):
    """
    Verifies that all CSV files in a directory have the same columns and data types.

    Args:
        directory (str): The path to the directory containing the CSV files.
    """
    csv_files = sorted([f for f in os.listdir(directory) if f.endswith('.csv')])
    if not csv_files:
        print("No CSV files found in the directory.")
        return

    # Use the first CSV file as the reference schema
    first_file_path = os.path.join(directory, csv_files[0])
    try:
        print(f"Reading reference file: {first_file_path}")
        reference_df = pd.read_csv(first_file_path, low_memory=False)
        reference_schema = reference_df.dtypes
        reference_columns = reference_df.columns
        print(f"Reference schema taken from: {csv_files[0]}")
        
    except Exception as e:
        print(f"Error reading reference file {first_file_path}: {e}")
        return

    all_match = True
    # Compare schema of other files with the reference
    for csv_file in csv_files[1:]:
        file_path = os.path.join(directory, csv_file)
        try:
            print(f"Reading file for comparison: {file_path}")
            current_df = pd.read_csv(file_path, low_memory=False)
            current_columns = current_df.columns

            # Check for column equality
            if not reference_columns.equals(current_columns):
                all_match = False
                print(f"--- MISMATCH FOUND in {csv_file} ---")
                print("Mismatched columns:")
                ref_set = set(reference_columns)
                curr_set = set(current_columns)
                
                missing_from_current = ref_set - curr_set
                if missing_from_current:
                    print(f"  Columns in reference but not in '{csv_file}': {sorted(list(missing_from_current))}")
                    added_in_current = curr_set - ref_set

                if added_in_current:
                    print(f"  Columns in '{csv_file}' but not in reference: {sorted(list(added_in_current))}")
                
                # We can stop checking this file if columns are different
                continue

            # Check for dtype equality if columns are the same
            current_schema = current_df.dtypes
            if not reference_schema.equals(current_schema):
                all_match = False
                print(f"--- MISMATCH FOUND in {csv_file} ---")
                print("Mismatched data types:")
                # Find and print differences
                for col in reference_schema.index:
                    if reference_schema[col] != current_schema[col]:
                        print(f"  Column '{col}':")
                        print(f"    - Reference ({csv_files[0]}): {reference_schema[col]}")
                        print(f"    - Current   ({csv_file}): {current_schema[col]}")
            
        except Exception as e:
            all_match = False
            print(f"Could not process file {file_path}: {e}")
    
    if all_match:
        print("Success! All CSV files have the same columns and data types.")
    else:
        print("Verification failed. One or more files have schema mismatches.")


if __name__ == "__main__":
    CLEANED_CSVS_DIR = 'clean_data/cleaned_csvs'
    verify_csv_schemas(CLEANED_CSVS_DIR)
