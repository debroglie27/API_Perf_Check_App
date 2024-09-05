import os
import re
import glob
import pandas as pd

# Define patterns for both formats
response_time_pattern_uwsgi = re.compile(r'generated \d+ bytes in (\d+) msecs')
response_time_pattern_nginx = re.compile(r'\*\*\*(\d+\.\d+)\*\*\*')

def average_response_time_uwsgi(file_path):
    """Parse uwsgi logs and calculate the average response time in milliseconds."""
    response_times = []
    with open(file_path, 'r') as file:
        for line in file:
            match = response_time_pattern_uwsgi.search(line)
            if match:
                response_times.append(int(match.group(1)))
    if response_times:
        return round(sum(response_times) / len(response_times))  # Round to nearest integer
    else:
        return None

def average_response_time_nginx(file_path):
    """Parse nginx logs and calculate the average response time in milliseconds."""
    response_times = []
    with open(file_path, 'r') as file:
        for line in file:
            match = response_time_pattern_nginx.search(line)
            if match:
                response_time_sec = float(match.group(1))  # Get time in seconds
                response_times.append(int(response_time_sec * 1000))  # Convert to milliseconds
    if response_times:
        return round(sum(response_times) / len(response_times))  # Round to nearest integer
    else:
        return None

def calculate_num_users_from_logs(log_folder):
    """Estimate the number of users based on the number of lines in one log file."""
    log_files = glob.glob(os.path.join(log_folder, "*.logs"))
    if log_files:
        first_log_file = log_files[0]  # Choose the first log file found
        try:
            with open(first_log_file, 'r') as file:
                total_lines = sum(1 for line in file)
            return total_lines
        except IOError as e:
            print(f"Error reading file {first_log_file}: {e}")
    return None

def find_folder(base_folder, prefix):
    """Find a folder that starts with the given prefix and ensure it's a directory."""
    folders = glob.glob(os.path.join(base_folder, f"{prefix}*"))
    for folder in folders:
        if os.path.isdir(folder):
            return folder
    return None

def process_folder(folder_path, prefix):
    """Process a folder to gather response times for either uwsgi or nginx logs."""
    log_files = {
        "1.login.logs": "login",
        "2.course_list.logs": "course_list",
        "3.quiz_list.logs": "quiz_list",
        "4.quiz_info.logs": "quiz_info",
        "5.quiz_download.logs": "quiz_download",
        "6.quiz_authenticate.logs": "quiz_authenticate",
        "7.quiz_submit.logs": "quiz_submit"
    }

    target_folder = find_folder(folder_path, prefix)
    if not target_folder:
        print(f"No valid '{prefix}' folder found in {folder_path}")
        return None

    # Calculate the number of users based on one log file
    num_users = calculate_num_users_from_logs(target_folder)
    if num_users is None:
        print(f"Unable to determine number of users for folder {folder_path}")
        return None

    results = {api_name: None for api_name in log_files.values()}
    for log_file, api_name in log_files.items():
        file_path = os.path.join(target_folder, log_file)
        if os.path.isfile(file_path):
            if prefix == "uwsgi":
                avg_response_time = average_response_time_uwsgi(file_path)
            else:  # For inner-nginx logs
                avg_response_time = average_response_time_nginx(file_path)
            
            if avg_response_time is not None:
                results[api_name] = avg_response_time
            else:
                results[api_name] = "No data"
        else:
            results[api_name] = "File not found"
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
    user_counts = sorted(set(result['Number of Users'] for result in all_results))
    
    # Initialize the DataFrame
    api_names = ["login", "course_list", "quiz_list", "quiz_info", "quiz_download", "quiz_authenticate", "quiz_submit"]
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
    # Find all "2024" folders in the current directory
    base_path = os.getcwd()  # Current working directory
    folders = glob.glob(os.path.join(base_path, "2024*"))

    # Process and save results for "uwsgi"
    process_and_save_results(folders, "uwsgi", 'uwsgi_response_times_summary.csv')

    # Process and save results for "inner-nginx"
    process_and_save_results(folders, "inner-nginx", 'nginx_response_times_summary.csv')

if __name__ == "__main__":
    main()
