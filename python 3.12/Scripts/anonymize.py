import pandas as pd
import numpy as np
import random
import string
from datetime import datetime, timedelta

# Function to anonymize data based on type
def anonymize_data(value, data_type):
    if pd.isna(value):
        return value
    
    if data_type.startswith('date'):
        # Extract date format from metadata (e.g., 'date(%Y-%m-%d)')
        date_format = data_type[5:-1]  # Removes 'date(' and ')'
        
        # Anonymize date by adding a random number of days
        original_date = datetime.strptime(str(value), date_format)
        random_days = random.randint(-365, 365)
        anonymized_date = original_date + timedelta(days=random_days)
        return anonymized_date.strftime(date_format)
    
    elif data_type == 'number':
        # Convert value to string for processing
        value_str = str(value)
        
        # Check if the original value is an integer or decimal
        if '.' in value_str:
            # Anonymize decimal by adding a random float offset and preserving decimal points
            decimal_points = len(value_str.split('.')[1])  # Count decimal points
            random_offset = random.uniform(-100, 100)
            anonymized_value = float(value_str) + random_offset
            # Format the anonymized value to match the original number of decimal points
            return f"{anonymized_value:.{decimal_points}f}"
        else:
            # Anonymize integer by adding a random integer offset
            random_offset = random.randint(-100, 100)
            return int(value_str) + random_offset
    
    elif data_type == 'alphanumeric':
        # Anonymize alphanumeric by generating a random string of the same length
        length = len(str(value))
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    else:
        # If data type is not recognized, return the original value
        return value

# Function to load metadata
def load_metadata(metadata_file):
    metadata = {}
    with open(metadata_file, 'r') as file:
        for line in file:
            column, data_type = line.strip().split('|')
            metadata[column] = data_type
    return metadata

# Main function to anonymize CSV
def anonymize_csv(input_csv, metadata_file, output_csv):
    # Load metadata
    metadata = load_metadata(metadata_file)
    
    # Load CSV file (assuming no header in the CSV)
    df = pd.read_csv(input_csv, delimiter='|', header=None)
    
    # Assign column names based on metadata keys
    df.columns = list(metadata.keys())
    
    # Anonymize each column based on metadata
    for column in df.columns:
        if column in metadata:
            df[column] = df[column].apply(lambda x: anonymize_data(x, metadata[column]))
    
    # Save anonymized data to new CSV
    df.to_csv(output_csv, sep='|', index=False, header=False)

# Example usage
input_csv = 'input.csv'
metadata_file = 'metadata.txt'
output_csv = 'anonymized_output.csv'

anonymize_csv(input_csv, metadata_file, output_csv)