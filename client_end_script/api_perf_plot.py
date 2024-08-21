import os
import pandas as pd
import matplotlib.pyplot as plt

# Directory containing the CSV files
directory = "./collected_csvs"

# Initialize dictionaries to hold the data
average_response_times = {}
failure_counts = {}
num_users_set = set()

# Extract data from each CSV file
for filename in os.listdir(directory):
    if filename.endswith("_stats.csv"):
        num_users = int(filename.split('_')[0])  # Extract the number of users from the filename
        num_users_set.add(num_users)  # Collect num_users for xticks
        file_path = os.path.join(directory, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Filter out the 'Aggregated' row
        df = df[df['Name'] != 'Aggregated']
        
        # Extract the API names, average response times, and failure counts
        for index, row in df.iterrows():
            api_name = row['Name']
            avg_response_time = row['Average Response Time']
            failure_count = row['Failure Count']
            
            # Store average response times
            if api_name not in average_response_times:
                average_response_times[api_name] = []
            average_response_times[api_name].append((num_users, avg_response_time))
            
            # Store failure counts
            if api_name not in failure_counts:
                failure_counts[api_name] = []
            failure_counts[api_name].append((num_users, failure_count))

# Sort the num_users for xticks
sorted_num_users = sorted(num_users_set)

# Plot average response times
plt.figure(figsize=(10, 6))
plt.title("Average Response Time vs. Number of Users")
for api_name, data in average_response_times.items():
    data.sort()  # Sort by num_users
    num_users = [item[0] for item in data]
    avg_response_time = [item[1] for item in data]
    plt.plot(num_users, avg_response_time, marker='o', label=api_name)

plt.xlabel("Number of Users")
plt.ylabel("Average Response Time (ms)")
plt.xticks(sorted_num_users)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('average_response_time_plot.png')

# Plot failure counts
plt.figure(figsize=(10, 6))
plt.title("Failure Count vs. Number of Users")
for api_name, data in failure_counts.items():
    data.sort()  # Sort by num_users
    num_users = [item[0] for item in data]
    failure_count = [item[1] for item in data]
    plt.plot(num_users, failure_count, marker='o', label=api_name)

plt.xlabel("Number of Users")
plt.ylabel("Failure Count")
plt.xticks(sorted_num_users)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('failure_count_plot.png')
