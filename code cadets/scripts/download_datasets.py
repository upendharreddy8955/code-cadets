import os
import requests

def download_file(url, folder, filename=None):
    """
    Downloads a file from a given URL to a specified folder.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    if filename is None:
        filename = url.split('/')[-1]

    filepath = os.path.join(folder, filename)

    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded {filename}.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

def main():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

    # Example datasets (replace with actual dataset URLs)
    # You will need to find appropriate datasets for drug interactions, dosages, etc.
    # For demonstration, I'm using placeholder URLs.
    datasets = [
        # {"url": "https://example.com/drug_interactions.csv", "filename": "drug_interactions.csv"},
        # {"url": "https://example.com/drug_dosages.json", "filename": "drug_dosages.json"},
        # {"url": "https://example.com/medication_alternatives.csv", "filename": "medication_alternatives.csv"},
    ]

    print("\n--- Starting Dataset Download ---")
    if not datasets:
        print("No dataset URLs provided. Please update 'download_datasets.py' with actual dataset URLs.")
    else:
        for dataset in datasets:
            download_file(dataset["url"], data_dir, dataset.get("filename"))
    print("--- Dataset Download Finished ---\n")

if __name__ == "__main__":
    main()