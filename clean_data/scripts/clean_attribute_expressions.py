def evaluate_attribute_expression(attribute_str):
    """
    Evaluates a FIFA attribute string (e.g., '75+2', '80') and returns an integer.
    Handles NaN values and coercing errors.
    """
    if pd.isna(attribute_str):
        return np.nan
    
    # Ensure it's a string for processing
    attribute_str = str(attribute_str).strip()

    if '+' in attribute_str:
        try:
            parts = attribute_str.split('+')
            base = int(float(parts[0]))  # Use float to handle potential "75.0+2"
            bonus = int(float(parts[1]))
            return base + bonus
        except ValueError:
            return np.nan
    else:
        try:
            return int(float(attribute_str)) # Handles cases like "80.0"
        except ValueError:
            return np.nan

def clean_attribute_expressions(df, columns):
    """
    Cleans specified columns in a DataFrame that contain FIFA attribute expressions
    (e.g., '75+2') by evaluating them to a single integer.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        columns (list): A list of column names to clean.

    Returns:
        pd.DataFrame: The DataFrame with cleaned attribute columns.
    """
    for col in columns:
        if col not in df.columns:
            print(f"Column '{col}' not found in DataFrame. Skipping.")
            continue
        
        # Apply the evaluation function
        df[col] = df[col].apply(evaluate_attribute_expression)
        
        # Convert to nullable integer type (Int64Dtype) to allow NaN values
        df[col] = df[col].astype(pd.Int64Dtype())
        
    return df

if __name__ == '__main__':
    # Create a sample DataFrame to demonstrate the function
    data = {
        'player': ['Player A', 'Player B', 'Player C', 'Player D', 'Player E'],
        'ls': ['75+2', '80', '60+5', np.nan, 'invalid'],
        'st': ['78+1', '82', '55', '70+3', 'abc'],
        'gk': ['10', '12+1', '8', '9+0', np.nan]
    }
    sample_df = pd.DataFrame(data)
    print("Original DataFrame:")
    print(sample_df)
    print("" + "="*30 + "")

    # The attribute columns to be cleaned
    attribute_cols = ['ls', 'st', 'gk']

    # Clean the attribute expressions
    cleaned_df = clean_attribute_expressions(sample_df.copy(), attribute_cols)
    
    print("Cleaned DataFrame:")
    print(cleaned_df)
    print("Data Types of Cleaned Columns:")
    print(cleaned_df[attribute_cols].dtypes)
    print("" + "="*30 + "")

    # Example with the actual project data
    # Assuming the combined_players_data.csv exists
    try:
        players_df = pd.read_csv('./clean_data/combined_players_data.csv')
        
        # Define the full list of positional rating columns
        positional_cols = [
            'ls', 'st', 'rs', 'lw', 'lf', 'cf', 'rf', 'rw', 'lam', 'cam', 'ram',
            'lm', 'lcm', 'cm', 'rcm', 'rm', 'lwb', 'ldm', 'cdm', 'rdm', 'rwb',
            'lb', 'lcb', 'cb', 'rcb', 'rb', 'gk'
        ]
        
        cleaned_players_df = clean_attribute_expressions(players_df.copy(), positional_cols)
        
        print("First 5 rows of the project DataFrame after applying cleaning function (positional attributes):")
        print(cleaned_players_df[positional_cols].head())
        print("Data Types of positional columns in project DataFrame:")
        print(cleaned_players_df[positional_cols].dtypes)

    except FileNotFoundError:
        print("Could not find './clean_data/combined_players_data.csv'.")
