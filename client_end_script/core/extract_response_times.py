import os
import re
import json


def process_file(file_path, respTimeRegex, timeUnit):
    """Extract response times from nginx logs and overwrite the file with only response times in milliseconds."""
    respTimePattern = re.compile(respTimeRegex)

    response_times = []
    with open(file_path, 'r') as file:
        for line in file:
            match = respTimePattern.search(line)
            if match:
                response_time = float(match.group(1))
                if timeUnit == "s":
                    response_time_ms = str(int(response_time * 1000))  # Convert to milliseconds
                else:
                    response_time_ms = str(int(response_time))  # Already in ms, So No Conversion

                response_times.append(response_time_ms)
    
    if response_times:
        with open(file_path, 'w') as file:
            file.write('\n'.join(response_times))


def process_folder(folder_path, component):
    """Process a folder and replace log files with only extracted response times."""

    componentName = component['name']
    componentRespTimeRegex = component['respTimeRegex']
    componentTimeUnit = component['timeUnit']

    # Load API information from JSON file
    with open('settings/APIs.json', 'r') as f:
        api_info = json.load(f)
    
    for api in api_info:
        log_file = api['id'] + "." + api['name'] + ".logs"
        file_path = os.path.join(folder_path, componentName, log_file)
        if os.path.isfile(file_path):
            process_file(file_path, componentRespTimeRegex, componentTimeUnit)
        else:
            print(f"File not found: {file_path}")


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
