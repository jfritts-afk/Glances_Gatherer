import os
import shutil
from datetime import datetime
import requests
import yaml

# Configuration
GLANCES_API_URL = "http://192.168.1.34:61208/api/4"
OUTPUT_FILE = "system_info.yaml"

# Define directory paths
most_recent_dir = 'most_recent_fetch'
old_fetch_dir = 'old_fetch_data'

# Ensure directories exist
os.makedirs(most_recent_dir, exist_ok=True)
os.makedirs(old_fetch_dir, exist_ok=True)

def get_glances_metrics():
    try:
        response = requests.get(f"{GLANCES_API_URL}/all")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching Glances data: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON from Glances data: {e}")
        return None

def save_to_yaml(data, file_name):
    try:
        with open(file_name, "w") as file:
            yaml.dump(data, file, default_flow_style=False)
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving to YAML: {e}")

def move_old_files():
    now = datetime.now()
    print(f"Current time: {now}")
    print(f"Files in '{most_recent_dir}': {os.listdir(most_recent_dir)}")
    for file in os.listdir(most_recent_dir):
        file_path = os.path.join(most_recent_dir, file)
        if os.path.isfile(file_path) and file.endswith('.yaml'):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"Checking file: {file_path}, last modified: {file_time}")
            if (now - file_time).total_seconds() > 15:  # 15 seconds old
                try:
                    print(f"Moving file: {file_path} to {old_fetch_dir}")
                    shutil.move(file_path, old_fetch_dir)
                except Exception as e:
                    print(f"Error moving file {file_path}: {e}")
            else:
                print(f"File is not old enough to move: {file_path}")

def main():
    collected_data = {}

    # Fetch system metrics from Glances
    glances_metrics = get_glances_metrics()
    if glances_metrics:
        collected_data['glances_metrics'] = glances_metrics
    else:
        collected_data['glances_metrics'] = "Failed to fetch data"

    # Include timestamp
    collected_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save collected data to a YAML file in the most recent directory
    current_file_path = os.path.join(most_recent_dir, OUTPUT_FILE)
    save_to_yaml(collected_data, current_file_path)

    # Move old files
    move_old_files()

if __name__ == "__main__":
    main()
