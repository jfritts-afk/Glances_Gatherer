# System Monitor Script

This Python script collects system metrics using Glances and checks for system updates using Cockpit. The collected data is saved in a YAML file for easy parsing.

## Features

- Fetches real-time system metrics via the Glances API.
- Checks for available system updates using Cockpit's API.
- Outputs all collected data to a YAML file for easy processing.

## Prerequisites

- **Glances** installed and running with the RESTful API enabled.
- **Cockpit** installed and accessible with the API enabled.
- Python packages: `requests`, `yaml`

## Configuration

- Update the `GLANCES_API_URL`, `COCKPIT_API_URL`, `COCKPIT_USERNAME`, and `COCKPIT_PASSWORD` variables in the script to match your setup.
- The output file is named `system_info.yaml` by default. You can change this by modifying the `OUTPUT_FILE` variable.

## Usage

1. Run the script:
    ```bash
    python system_monitor.py
    ```
2. The script will generate a `system_info.yaml` file containing the system metrics and update information.

## Output

The output is saved in a YAML file format, which includes:
- **System metrics** fetched from Glances.
- **System updates** fetched from Cockpit.
- **Timestamp** of when the data was collected.

## License

This project is licensed under the MIT License.
