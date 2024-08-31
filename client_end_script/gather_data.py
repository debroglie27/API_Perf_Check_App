import os
import re
import glob
import pandas as pd

# Define a pattern to match response times
response_time_pattern = re.compile(r'generated \d+ bytes in (\d+) msecs')

def average_response_time(file_path):
    response_times = []
    with open(file_path, 'r') as file:
        for line in file:
            match = response_time_pattern.search(line)
            if match:
                response_times.append(int(match.group(1)))
    if response_times:
        return round(sum(response_times) / len(response_times))  # Round to nearest integer
    else:
        return None

def calculate_num_users_from_logs(log_folder):
    """Estimate number of users based on the number of lines in one log file."""
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

def find_uwsgi_folder(base_folder):
    """Find the uwsgi folder that starts with 'uwsgi' and ensure it's a directory."""
    uwsgi_folders = glob.glob(os.path.join(base_folder, "uwsgi*"))
    for folder in uwsgi_folders:
        if os.path.isdir(folder):
            return folder
    return None

def process_folder(folder_path):
    log_files = {
        "1.login.logs": "login",
        "2.course_list.logs": "course_list",
        "3.quiz_list.logs": "quiz_list",
        "4.quiz_info.logs": "quiz_info",
        "5.quiz_download.logs": "quiz_download",
        "6.quiz_authenticate.logs": "quiz_authenticate",
        "7.quiz_submit.logs": "quiz_submit"
    }

    uwsgi_folder = find_uwsgi_folder(folder_path)
    if not uwsgi_folder:
        print(f"No valid 'uwsgi' folder found in {folder_path}")
        return None

    # Calculate the number of users based on one log file
    num_users = calculate_num_users_from_logs(uwsgi_folder)
    if num_users is None:
        print(f"Unable to determine number of users for folder {folder_path}")
        return None

    results = {api_name: None for api_name in log_files.values()}
    for log_file, api_name in log_files.items():
        file_path = os.path.join(uwsgi_folder, log_file)
        if os.path.isfile(file_path):
            avg_response_time = average_response_time(file_path)
            if avg_response_time is not None:
                results[api_name] = avg_response_time
            else:
                results[api_name] = "No data"
        else:
            results[api_name] = "File not found"
    results['Number of Users'] = num_users
    return results

def main():
    # Find all "2024" folders in the current directory
    base_path = os.getcwd()  # Current working directory
    folders = glob.glob(os.path.join(base_path, "2024*"))

    all_results = []
    for folder in folders:
        results = process_folder(folder)
        if results:
            all_results.append(results)
            print(f"Processed folder {folder}: {results}")

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
    print("DataFrame:")
    print(df)  # Print DataFrame to check values before saving
    df.to_csv('response_times_summary.csv', index=False)
    print("Results have been saved to 'response_times_summary.csv'.")

if __name__ == "__main__":
    main()
