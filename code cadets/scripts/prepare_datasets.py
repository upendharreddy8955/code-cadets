import pandas as pd
import os

def load_dataset(filepath):
    """
    Loads a dataset from the given filepath.
    Supports CSV and JSON for now.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return None

    if filepath.endswith('.csv'):
        return pd.read_csv(filepath)
    elif filepath.endswith('.json'):
        return pd.read_json(filepath)
    else:
        print(f"Unsupported file format: {filepath}")
        return None

def clean_data(df):
    """
    Placeholder for data cleaning operations.
    e.g., handling missing values, removing duplicates, correcting data types.
    """
    if df is None:
        return None
    print("Cleaning data...")
    # Example: Drop rows with any missing values
    df = df.dropna()
    # Example: Remove duplicates
    df = df.drop_duplicates()
    return df

def transform_data(df):
    """
    Placeholder for data transformation operations.
    e.g., feature engineering, normalization, one-hot encoding.
    """
    if df is None:
        return None
    print("Transforming data...")
    # Example: Convert all column names to lowercase
    df.columns = df.columns.str.lower()
    return df

def main():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    processed_data_dir = os.path.join(data_dir, 'processed')

    if not os.path.exists(processed_data_dir):
        os.makedirs(processed_data_dir)

    # List of datasets to process (replace with your actual downloaded files)
    datasets_to_process = [
        # "drug_interactions.csv",
        # "drug_dosages.json",
        # "medication_alternatives.csv",
    ]

    print("\n--- Starting Dataset Mapping and Preparation ---")
    if not datasets_to_process:
        print("No datasets specified for processing. Please ensure you have downloaded datasets and updated 'prepare_datasets.py'.")
    else:
        for dataset_name in datasets_to_process:
            filepath = os.path.join(data_dir, dataset_name)
            print(f"Processing {dataset_name}...")
            df = load_dataset(filepath)
            if df is not None:
                df_cleaned = clean_data(df)
                df_transformed = transform_data(df_cleaned)

                if df_transformed is not None:
                    output_filepath = os.path.join(processed_data_dir, f"processed_{dataset_name}")
                    # Example: Save processed data back to CSV
                    df_transformed.to_csv(output_filepath, index=False)
                    print(f"Processed data saved to {output_filepath}")
    print("--- Dataset Mapping and Preparation Finished ---\n")

if __name__ == "__main__":
    main()