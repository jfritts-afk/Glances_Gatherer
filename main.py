import requests
import yaml
from datetime import datetime

# Configuration
GLANCES_API_URL = "http://192.168.1.34:61208/api/4"  # Replace with your Glances API URL
COCKPIT_API_URL = "http://localhost:9090"  # Replace with your Cockpit API URL
COCKPIT_USERNAME = "your_username"
COCKPIT_PASSWORD = "your_password"
OUTPUT_FILE = "system_info.yaml"

# Function to fetch system metrics from Glances
def get_system_metrics():
    try:
        response = requests.get(f"{GLANCES_API_URL}/all")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching Glances data: {e}")
        return None

# Function to authenticate with Cockpit
def authenticate_cockpit():
    try:
        response = requests.post(
            f"{COCKPIT_API_URL}/login",
            json={"user": COCKPIT_USERNAME, "password": COCKPIT_PASSWORD},
        )
        response.raise_for_status()
        return response.cookies
    except requests.RequestException as e:
        print(f"Error authenticating with Cockpit: {e}")
        return None

# Function to check for system updates using Cockpit
def check_system_updates(cookies):
    try:
        response = requests.get(
            f"{COCKPIT_API_URL}/pkg/list-updates", cookies=cookies
        )
        response.raise_for_status()
        updates = response.json().get("updates", [])
        return updates
    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")
        return None

# Function to save data to a YAML file
def save_to_yaml(data, file_name):
    try:
        with open(file_name, "w") as file:
            yaml.dump(data, file, default_flow_style=False)
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving to YAML: {e}")

# Main function
def main():
    # Dictionary to store all the collected data
    collected_data = {}

    # Step 1: Fetch system metrics from Glances
    system_metrics = get_system_metrics()
    if system_metrics:
        collected_data['system_metrics'] = system_metrics
    
    # Step 2: Authenticate with Cockpit
    cockpit_cookies = authenticate_cockpit()
    if cockpit_cookies:
        # Step 3: Check for system updates
        updates = check_system_updates(cockpit_cookies)
        if updates:
            collected_data['system_updates'] = updates
        else:
            collected_data['system_updates'] = "No updates available."

    # Add a timestamp to the collected data
    collected_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Step 4: Save collected data to a YAML file
    save_to_yaml(collected_data, OUTPUT_FILE)

if __name__ == "__main__":
    main()
