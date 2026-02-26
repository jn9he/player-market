import pandas as pd
import os
import glob

def clean_dataframe(df):
    """
    Cleans the FIFA dataset by removing goalkeepers, dropping unnecessary columns,
    and converting attribute columns to numeric types.
    """
    # Drop goalkeepers if 'player_positions' column exists
    if 'player_positions' in df.columns:
        df = df[df['player_positions'] != 'GK'].copy()

    # Define columns to drop
    columns_to_drop = [
        'club_loaned_from', 'nation_team_id', 'nation_position',
        'nation_jersey_number', 'release_clause_eur', 'player_tags', 'player_traits',
        'mentality_composure', 'goalkeeping_speed',
        'nation_logo_url', 'club_logo_url', 'club_flag_url',
        'value_eur', 'wage_eur', 'club_team_id', 'club_name', 'league_name', 'league_level',
        'club_position', 'club_jersey_number', 'club_joined', 'club_contract_valid_until',
        'goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking',
        'goalkeeping_positioning', 'goalkeeping_reflexes', 'player_face_url', 'nation_flag_url',
        'gk'  # This was a separate step in the notebook
    ]
    
    # Drop columns that exist in the dataframe
    existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    df = df.drop(columns=existing_columns_to_drop)

    # Convert player attribute columns from string expressions (e.g., '60+2') to integers
    columns_to_convert = [
        'ls', 'st', 'rs', 'lw', 'lf', 'cf', 'rf', 'rw', 'lam', 'cam', 'ram',
        'lm', 'lcm', 'cm', 'rcm', 'rm', 'lwb', 'ldm', 'cdm', 'rdm', 'rwb',
        'lb', 'lcb', 'cb', 'rcb', 'rb'
    ]
    
    for col in columns_to_convert:
        if col in df.columns:
            # Use eval to solve the string expression, then convert to int
            df[col] = df[col].apply(eval).astype(int)

    return df

def main():
    """
    Main function to find all player CSVs, clean them, and save them to a new directory.
    """
    input_dir = 'fifa-dataset'
    output_dir = 'clean_data/cleaned_csvs'
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all player CSV files
    csv_files = glob.glob(os.path.join(input_dir, 'players_*.csv'))
    
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return

    for file_path in csv_files:
        print(f"Processing {file_path}...")
        try:
            # Use low_memory=False to avoid DtypeWarning
            df = pd.read_csv(file_path, low_memory=False)
            
            cleaned_df = clean_dataframe(df)
            
            # Construct output path and save the cleaned file
            file_name = os.path.basename(file_path)
            output_file_path = os.path.join(output_dir, file_name)
            cleaned_df.to_csv(output_file_path, index=False)
            
            print(f"Successfully cleaned and saved to {output_file_path}")
        
        except Exception as e:
            print(f"Could not process {file_path}. Error: {e}")

if __name__ == '__main__':
    main()
