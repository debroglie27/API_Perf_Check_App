import os
import re
import json


def extract_api_specific_logs(filename, dirname):
    """
    Extracts and organizes logs for specific APIs into separate files based on search terms defined in a JSON configuration file.

    Args:
        filename (str): The path to the log file containing all logs.
        dirname (str): The directory where API-specific log files will be created.

    Functionality:
        1. Loads API information from a JSON file located at 'settings/APIs.json'. The JSON file should have the following structure:
        [
            {
                "apiID": "ID of the API",
                "apiName": "Name of the API",
                "searchTerm": "Regex pattern to identify logs for this API"
            },
            ...
        ]
        2. Creates the specified directory (`dirname`) if it does not already exist.
        3. Reads all log entries from the provided log file (`filename`).
        4. Iterates through the list of APIs from the JSON file and uses the `searchTerm` to filter logs relevant to each API.
        5. Writes the filtered logs into separate files named `<apiID>.<apiName>.logs` in the specified directory.
    """

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
        api_logfile = os.path.join(dirname, f"{api['id']}.{api['name']}.logs")
        with open(api_logfile, 'w') as api_file:
            api_file.writelines(matching_logs)


def organize_logs(test_id):
    """
    Extracts and organizes log data for each component based on a test ID and a JSON configuration file.

    Args:
        test_id (str): The unique identifier for the test, used to locate and organize component-specific logs.

    Functionality:
        1. Loads component information from a JSON file located at 'settings/components.json'. The JSON file should have the following structure:
           [
               {
                   "componentName": "Name of the component"
                   ...
               },
               ...
           ]
        2. Iterates through the list of components in the JSON file.
        3. For each component:
           - Constructs the log file path using the pattern `<test_id>/<componentName>-<test_id>.log`.
           - Constructs the output directory path using the pattern `<test_id>/<componentName>`.
           - Calls the `extract_api_specific_logs` function to extract API-specific logs for the component, using the constructed paths.
    """

    with open('settings/components.json','r') as f:
        components_info = json.load(f)
    
    for component in components_info:
        filename=test_id+"/"+component["name"]+"-"+test_id+".log"
        dirname=test_id+"/"+component["name"]

        extract_api_specific_logs(filename,dirname)
