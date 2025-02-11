import os
import csv
import json
import glob
import pandas as pd


def average_response_time(file_path, api_name):
    """Parse uwsgi logs and calculate the average response time in milliseconds for a given API name."""
    response_times = []
    
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        
        if api_name not in reader.fieldnames:
            raise ValueError(f"API name '{api_name}' not found in CSV columns.")
        
        for row in reader:
            if row[api_name]:  # Ensure the value exists
                response_times.append(int(row[api_name]))  # Convert string to integer
    
    if response_times:
        return round(sum(response_times) / len(response_times))  # Round to nearest integer
    else:
        return None


def calculate_num_users_from_logs(file_path):
    """Estimate the number of users based on the number of lines in one log file."""
    try:
        with open(file_path, 'r') as file:
            total_lines = sum(1 for _ in file)

        return total_lines-1

    except IOError as e:
        print(f"Error reading file {file_path}: {e}")

    return None


def process_folder(folder_path, prefix):
    """Process a folder to gather response times for either uwsgi or nginx logs."""
    # Load API information from JSON file
    with open('./settings/APIs.json', 'r') as f:
        api_info = json.load(f)

    csv_file = prefix + "_response_times.csv"
    file_path = os.path.join(folder_path, csv_file)

    if not os.path.isfile(file_path):
        return None

    # Calculate the number of users based on one log file
    num_users = calculate_num_users_from_logs(file_path)
    if num_users is None:
        print(f"Unable to determine number of users for folder {folder_path}")
        return None

    results = {api['name']: None for api in api_info}
    for api in api_info:
        avg_response_time = average_response_time(file_path, api['name'])
        results[api['name']] = avg_response_time
        
    results['Number of Users'] = num_users

    return results


def process_and_save_results(folders, prefix, output_filename):
    """Process folders and save the results in a CSV file for either uwsgi or nginx."""
    all_results = []
    for folder in folders:
        results = process_folder(folder, prefix)
        if results:
            all_results.append(results)
            print(f"Processed folder {folder} for {prefix}: {results}")

    # Collect all unique number of users and sort them
    user_counts = sorted({result['Number of Users'] for result in all_results})
    
    # Initialize the DataFrame
    # Load API information from JSON file
    with open('./settings/APIs.json', 'r') as f:
        api_info = json.load(f)
    
    api_names = [api['name'] for api in api_info]
    columns = ['API_name'] + [f'RespTime_{count}(ms)' for count in user_counts]
    
    # Prepare data for DataFrame
    df_data = []
    for api_name in api_names:
        row = [api_name]
        for user_count in user_counts:
            matching_results = [result[api_name] for result in all_results if result['Number of Users'] == user_count]
            if matching_results:
                row.append(matching_results[0])
            else:
                row.append(None)  # Fill with None if no data available for that user count
        df_data.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(df_data, columns=columns)
    
    # Ensure the directory "consolidated_results" exists
    os.makedirs('consolidated_results', exist_ok=True)
    
    # Save the CSV file in the "consolidated_results" folder
    output_path = os.path.join('consolidated_results', output_filename)
    print(f"DataFrame for {prefix}:")
    print(df)  # Print DataFrame to check values before saving
    df.to_csv(output_path, index=False)
    print(f"Results have been saved to '{output_path}'.")


def main():
    # Find all "2025" folders in the current directory
    base_path = os.getcwd()  # Current working directory
    folders = glob.glob(os.path.join(base_path, "2025*"))

    # Process and save results for "uwsgi"
    process_and_save_results(folders, "uwsgi", 'uwsgi_response_times_summary.csv')

    # Process and save results for "inner-nginx"
    process_and_save_results(folders, "inner-nginx", 'nginx_response_times_summary.csv')


if __name__ == "__main__":
    main()
