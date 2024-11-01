from kaggle.api.kaggle_api_extended import KaggleApi
import os
from datetime import datetime

# Initialize API
api = KaggleApi()
api.authenticate()

today_date = datetime.today().strftime('%Y-%m-%d')
# Path to the CSV file you want to upload
file_path = f'data'
dataset_slug = "nabinoli2004/kalimati-vegetable-datasets-nepal"  # Your existing dataset slug (username/dataset-name)

# Update the dataset by uploading a new version
try:
    api.dataset_create_version(file_path, version_notes=f"Updated commodity prices data for {today_date}", delete_old_versions=False)
    print("Dataset updated successfully!")
except Exception as e:
    print("Exception when updating dataset:", e)
