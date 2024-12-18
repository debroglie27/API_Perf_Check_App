import os
import re
import json


def extract_api_specific_logs(filename, dirname):
    # Load API information from JSON file
    with open('settings/APIs.json', 'r') as f:
        api_info = json.load(f)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    
    # Open the log file for reading
    with open(filename, 'r') as logfile:
        logs = logfile.readlines()  # Read all lines from the log file
    
    # Loop through the API info and extract relevant logs using regex
    for api in api_info:
        search_term = api['searchTerm']
        pattern = re.compile(search_term)  # Compile the search term as a regex pattern
        matching_logs = [log for log in logs if pattern.search(log)]  # Filter logs using regex search
        
        # Write the matching logs to the API-specific file
        api_logfile = os.path.join(dirname, f"{api['APIName']}.logs")
        with open(api_logfile, 'w') as api_file:
            api_file.writelines(matching_logs)


def extract_data(test_id):
    with open('settings/components.json','r') as f:
        components_info = json.load(f)
    
    for item in components_info:
        filename=test_id+"/"+item["componentName"]+"-"+test_id+".log"
        dirname=test_id+"/"+item["componentName"]

        extract_api_specific_logs(filename,dirname)