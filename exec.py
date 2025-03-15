import os
import shutil
import kagglehub
import pandas as pd
import dask.dataframe as dd
import time
from memory_profiler import memory_usage
import gc
import glob
import datetime

# Define the path to kaggle.json (same directory as the notebook)
json_path = os.path.join(os.getcwd(), "kaggle.json")

# Move it to the correct Kaggle API location
os.makedirs(os.path.expanduser("~/.kaggle"), exist_ok=True)
os.system(f"cp {json_path} ~/.kaggle/")

# Set correct permissions
os.system("chmod 600 ~/.kaggle/kaggle.json")

print("Kaggle authentication set up successfully!")


# Define the new .kaggle directory inside the working directory
new_dir = os.path.join(os.getcwd(), ".kaggle")

# Create the kaggle directory if it doesn't exist
os.makedirs(new_dir, exist_ok=True)

# Move kaggle.json to the correct location
shutil.move("kaggle.json", os.path.join(new_dir, "kaggle.json"))

# Set the correct permissions
os.chmod(os.path.join(new_dir, "kaggle.json"), 0o600)

print(f"Kaggle authentication file moved to: {new_dir}")


# Download latest version
path = kagglehub.dataset_download("mkechinov/ecommerce-behavior-data-from-multi-category-store")

print("Path to dataset files:", path)

dataset_path = "/root/.cache/kagglehub/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store/versions/8"

# List all files
for root, dirs, files in os.walk(dataset_path):
    for file in files:
        print(os.path.join(root, file))
        
        
        
# Find all CSV files in the dataset folder
csv_files = glob.glob(os.path.join(dataset_path, "*.csv"))

# Function to convert 'YYYY-MMM.csv' to a comparable datetime format
def extract_date(filename):
    base_name = os.path.basename(filename).replace(".csv", "")  # Remove path and .csv
    year, month_abbr = base_name.split("-")  # Split by "-"
    month_number = datetime.datetime.strptime(month_abbr, "%b").month  # Convert 'Oct' → 10
    return datetime.datetime(int(year), month_number, 1)  # Return a datetime object

# Get the latest file by sorting filenames (assuming format 'YYYY-MM.csv')
latest_file = max(csv_files, key=os.path.getctime)

print(f"Processing latest file: {latest_file}")

chunk_size = 500_000  
sample_fraction = 0.1  # 10% of data

chunks = []
for chunk in pd.read_csv(latest_file, chunksize=chunk_size):
    sampled_chunk = chunk.sample(frac=sample_fraction, random_state=42)  # Ensures reproducibility
    chunks.append(sampled_chunk)

sampled_data = pd.concat(chunks, ignore_index=True)
sampled_data.to_csv("sampled_ecommerce_data.csv", index=False)

print("Sampled dataset saved.")

file_path = os.path.join('sampled_ecommerce_data.csv')
chunk_size = 500_000  # Adjust based on memory usage
output_file = "cleaned_ecommerce_data.csv"

first_chunk = True  # To handle writing headers correctly
event_counter = 0  # Start event_id counter

for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    # Convert event_time to datetime
    chunk["event_time"] = pd.to_datetime(chunk["event_time"], errors="coerce")

    # Remove duplicates
    chunk.drop_duplicates(inplace=True)

    # Drop category_code and handle missing brand values
    chunk.drop(columns=["category_code"], inplace=True)
    chunk.loc[:, "brand"] = chunk["brand"].fillna("Unavailable")

    # Assign unique event_id
    chunk["event_id"] = range(event_counter, event_counter + len(chunk))
    event_counter += len(chunk)  # Update the counter for the next chunk

    # Save chunk to file
    chunk.to_csv(output_file, mode="w" if first_chunk else "a", header=first_chunk, index=False)

    first_chunk = False  # Set to False after first write
    del chunk  # Free memory
    gc.collect()


chunk_size = 500_000
selected_cols = ["event_time", "event_type", "product_id", "brand", "price"]

chunks = []
for chunk in pd.read_csv("cleaned_ecommerce_data.csv", usecols=selected_cols, chunksize=chunk_size):
    chunks.append(chunk.sample(frac=0.1))  # Load only 10% of each chunk (adjust as needed)

df = pd.concat(chunks, ignore_index=True)


print(df.info())  # Check data types & missing values
print(df.describe())  # Summary stats for numerical columns
print(df["event_type"].value_counts())  # Count of each event type