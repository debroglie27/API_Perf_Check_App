#!/usr/bin/env python3

import os
import pandas as pd
import matplotlib.pyplot as plt

# Directory where the collected CSVs are stored
csv_dir = './collected_csvs'

# Dictionary to store data
data = {}
num_users_list = []

# Loop through each CSV file in the directory
for csv_file in os.listdir(csv_dir):
    if csv_file.endswith('_stats.csv'):
        # Extract the number of users from the filename
        num_users = int(csv_file.split('_')[0])
        num_users_list.append(num_users)
        
        # Read the CSV file
        df = pd.read_csv(os.path.join(csv_dir, csv_file))
        
        # Loop through each row in the dataframe to extract the API name and average response time
        for _, row in df.iterrows():
            api_name = row['Name']
            avg_response_time = row['Average Response Time']
            
            # Skip the "Aggregated" row
            if pd.notna(api_name) and api_name != "Aggregated":  # Ensure the API name is not NaN and not "Aggregated"
                if api_name not in data:
                    data[api_name] = []
                data[api_name].append((num_users, avg_response_time))

# Plotting the data
plt.figure(figsize=(10, 6))
for api_name, values in data.items():
    values.sort()  # Sort values by number of users
    users, response_times = zip(*values)
    plt.plot(users, response_times, marker='o', label=api_name)

# Adding labels and title
plt.xlabel('Number of Users')
plt.ylabel('Average Response Time (ms)')
plt.title('Average Response Time vs Number of Users')

# Setting xticks dynamically based on num_users_list
plt.xticks(sorted(num_users_list))

# Adding grid and legend
plt.grid(True)
plt.legend()

# Save the plot to a file
plt.savefig('api_performance_plot.png')
