# Importing regular expression python module
import re
import json
import pandas as pd
import sys
import os
from scipy.stats import zscore

# Check if the correct number of arguments is provided
if len(sys.argv) != 6:
    print("Usage: python main.py <file_route> <records_to_filter> <anomalies_threshold> <bf_threshold>")
    sys.exit(1)

# Access command-line arguments
file_route = sys.argv[1]  # First argument
json_route = sys.argv[2] 
records_to_filter = int(sys.argv[3])  # second argument
anomalies_threshold = int(sys.argv[4]) # third argument
bf_threshold = int(sys.argv[5]) # for argument

# Check if the file exists
if not os.path.isfile(file_route):
    print(f"Error: File '{file_route}' does not exist.")
    sys.exit(1)

# Check if records_to_filter, anomalies_threshold, and bf_threshold are integers
try:
    records_to_filter = int(records_to_filter)
    anomalies_threshold = int(anomalies_threshold)
    bf_threshold = int(bf_threshold)
except ValueError:
    print("Error: records_to_filter, anomalies_threshold, and bf_threshold must be integers.")
    sys.exit(1)
  
# Create the output directory if it doesn't exist
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
        
 # Create an empty list to store JSON objects 
json_array = []

count = 0

# Read data
with open(file_route, 'r') as file:
    # Read each line of the file
    for line in file:
        # Regular expression pattern to extract relevant data
        pattern = r'(\S+) - - \[([\w:/]+\s[+\-]\d{4})\] "(GET|POST|PUT|DELETE|PATCH) (.+?)" (\d+)'
        # Finding all possible matches using regular expression
        matches = re.findall(pattern, line)
        for match in matches:
            # Collecting the results
            ip,timestamp, method, request, status = match
            # Create a dictionary representing a JSON object
            json_object = {
                "ip": ip,
                "timestamp": timestamp,
                "method": method,
                "request": request,
                "status": status
            }    
            # Insert the dictionary into the array    
            json_array.append(json_object)
        
        count = count + 1
        
        # This is a break condition because we have a lot of records
        if count == records_to_filter:
            break
        
        
# Creating a Dataframe with the filtered data 
df = pd.DataFrame(json_array)

# Group data by IP address and HTTP method, count requests
grouped = df.groupby(['ip', 'method']).size().reset_index(name='request_count')

# Convert the DataFrame to JSON format
json_result = grouped.to_json(orient='records')

# Write the JSON to a file
with open(json_route, 'w') as file:
    file.write(json_result)


df = pd.DataFrame(grouped)

# Calculate the z-score for request_count
df['request_count_zscore'] = zscore(df['request_count'])

# Define a threshold for anomalies (e.g., z-score greater than 3)
threshold = anomalies_threshold

# Identify anomalies
anomalies = df[df['request_count_zscore'] > threshold]

# Calculate the proportion of anomalies
proportion_anomalies = len(anomalies) / len(df)* 100

print("Proportion of anomalies found:", proportion_anomalies)

# Define a threshold for the number of requests to consider as a brute force attack
brute_force_threshold = bf_threshold

# Group DataFrame by IP address and sum the request counts
ip_request_counts = df.groupby('ip')['request_count'].sum()

# Identify potential brute force attacks
potential_brute_force = ip_request_counts[ip_request_counts > brute_force_threshold]

# Print IP addresses involved in potential brute force attacks
if not potential_brute_force.empty:
    print("Potential Brute Force Attacks:")
    print(potential_brute_force)
else:
    print("No potential brute force attacks detected.")

            