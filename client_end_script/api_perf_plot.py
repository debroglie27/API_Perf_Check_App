import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = {
    'API_name': ['login', 'course_list', 'quiz_list', 'quiz_info', 'quiz_download', 'quiz_authenticate', 'quiz_submit'],
    'RespTime_11(ms)': [651, 30, 120, 289, 29, 79, 38],
    'RespTime_22(ms)': [702, 28, 263, 370, 28, 134, 39],
    'RespTime_33(ms)': [656, 27, 153, 293, 27, 192, 36],
    'RespTime_40(ms)': [660, 26, 146, 289, 26, 88, 35],
    'RespTime_50(ms)': [699, 26, 270, 307, 26, 119, 36],
    'RespTime_60(ms)': [643, 24, 167, 274, 26, 100, 35],
    'RespTime_70(ms)': [639, 23, 183, 279, 25, 96, 36],
    'RespTime_80(ms)': [686, 23, 209, 323, 25, 106, 36],
    'RespTime_90(ms)': [643, 24, 175, 274, 25, 127, 36],
    'RespTime_100(ms)': [637, 24, 167, 275, 25, 108, 35]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Extract the number of users from column names
user_counts = [11, 22, 33, 40, 50, 60, 70, 80, 90, 100]

# Set the API_name as index
df.set_index('API_name', inplace=True)

# Plot
plt.figure(figsize=(12, 8))
for api_name in df.index:
    plt.plot(user_counts, df.loc[api_name], marker='o', label=api_name)

plt.xlabel('Number of Users')
plt.ylabel('Average Response Time (ms)')
plt.title('Average Response Times by Number of Users')
plt.legend(title='API Name')
plt.grid(True)
plt.xticks(user_counts)
plt.tight_layout()

# Save the plot as an image file
plt.savefig('response_times_plot.png')

# Show the plot
# plt.show()
