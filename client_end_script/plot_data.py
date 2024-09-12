import pandas as pd
import matplotlib.pyplot as plt

def plot_response_times(csv_file, title, output_file):
    # Load the CSV data into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract the number of users from the column names (ignore the first 'API_name' column)
    num_users = [int(col.split('_')[1].replace('(ms)', '')) for col in df.columns[1:]]

    # Plot each API response time against the number of users
    plt.figure(figsize=(10, 6))
    
    for index, row in df.iterrows():
        plt.plot(num_users, row[1:], marker='o', label=row['API_name'])
    
    plt.title(title)
    plt.xlabel('Number of Users')
    plt.ylabel('Response Time (ms)')
    plt.legend(title="API", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)

    # Set the x-ticks to be the number of users
    plt.xticks(num_users)
    
    plt.tight_layout()

    # Save the plot to the specified output file
    plt.savefig(output_file)
    plt.close()  # Close the figure to free memory

# Save the plot for uwsgi
plot_response_times('consolidated_results/uwsgi_response_times_summary.csv', 'UWSGI API Response Times', 'consolidated_results/uwsgi_response_times_plot.png')

# Save the plot for nginx
plot_response_times('consolidated_results/nginx_response_times_summary.csv', 'Nginx API Response Times', 'consolidated_results/nginx_response_times_plot.png')
