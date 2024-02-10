import sqlite3
def print_col(obj):
    for item in obj:
        print(item,end='\t')
    print()
# Connect to the SQLite database
conn = sqlite3.connect('testdates.db')  # Replace 'your_database.db' with your actual database file

print()
# Create a cursor object
cursor = conn.cursor()

# Specify the table name
table_name = 'test'  # Replace 'your_table_name' with the actual table name

# Execute the PRAGMA query to get column information
cursor.execute(f"PRAGMA table_info({table_name})")

# Fetch all rows from the result set
columns = cursor.fetchall()

# Extract and print column names
column_names = [column[1] for column in columns]
print_col(column_names)

cursor.execute(f"SELECT * FROM {table_name} where id =120 LIMIT 1")

# Fetch all rows from the result set
entries = cursor.fetchall()

# Print the top 3 entries
for entry in entries:
    print_col(entry)


# Close the cursor and connection
cursor.close()
conn.close()

print()