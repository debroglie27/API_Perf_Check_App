import os
import re
import csv
import json


def process_file(file_path, resp_time_regex, time_unit):
    """Extract response times from nginx logs and overwrite the file with only response times in milliseconds."""
    respTimePattern = re.compile(resp_time_regex)

    response_times = []
    with open(file_path, 'r') as file:
        for line in file:
            match = respTimePattern.search(line)
            if match:
                response_time = float(match.group(1))
                if time_unit == "s":
                    response_time_ms = str(int(response_time * 1000))  # Convert to milliseconds
                else:
                    response_time_ms = str(int(response_time))  # Already in ms, So No Conversion

                response_times.append(response_time_ms)
    
    return response_times


def write_response_times_to_csv(folder_path, component_name, api_names, response_data):
    """Writes response times to a CSV file."""
    max_length = max((len(times) for times in response_data.values()), default=0)
    csv_file_path = os.path.join(folder_path, f"{component_name}_response_times.csv")
    
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(api_names)  # Write header row with API names
        
        for i in range(max_length):
            row = [response_data[api][i] if i < len(response_data[api]) else '' for api in api_names]
            writer.writerow(row)
    
    print(f"Response times CSV created for {component_name} component")


def process_folder(folder_path, component):
    """Process a folder and replace log files with only extracted response times."""

    component_name = component['name']
    component_resp_time_regex = component['respTimeRegex']
    component_time_unit = component['timeUnit']

    # Load API information from JSON file
    with open('settings/APIs.json', 'r') as f:
        api_info = json.load(f)

    response_data = {}
    api_names = []
    
    for api in api_info:
        log_file = api['id'] + "." + api['name'] + ".logs"
        file_path = os.path.join(folder_path, component_name, log_file)

        if os.path.isfile(file_path):
            response_times = process_file(file_path, component_resp_time_regex, component_time_unit)
            response_data[api['name']] = response_times
            api_names.append(api['name'])
        else:
            print(f"File not found: {file_path}")

    write_response_times_to_csv(folder_path, component_name, api_names, response_data)


def extract_response_times(test_id):
    """Process the given test_id folder."""
    base_path = os.getcwd()
    folder = os.path.join(base_path, test_id)
    
    if os.path.isdir(folder):
        with open('settings/components.json','r') as f:
            components_info = json.load(f)

        for component in components_info:
            process_folder(folder, component)

        print(f"Processing completed for '{test_id}' folder.")
    else:
        print(f"Folder '{test_id}' not found.")
