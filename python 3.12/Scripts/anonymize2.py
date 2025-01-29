import pandas as pd
import numpy as np
import random
import string
from datetime import datetime, timedelta

# Function to anonymize data based on type
def anonymize_data(value, data_type):
    if pd.isna(value):
        return value
    
    if data_type == 'date':
        # Anonymize date by adding a random number of days
        original_date = datetime.strptime(value, '%Y-%m-%d')
        random_days = random.randint(-365, 365)
        anonymized_date = original_date + timedelta(days=random_days)
        return anonymized_date.strftime('%Y-%m-%d')
    
    elif data_type == 'number':
        # Anonymize number by adding a random offset
        random_offset = random.uniform(-100, 100)
        return float(value) + random_offset
    
    elif data_type == 'alphanumeric':
        # Anonymize alphanumeric by generating a random string of the same length
        length = len(value)
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