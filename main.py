# Importing regular expression python module
import re
import json
import pandas as pd
from scipy.stats import zscore

 # Create an empty list to store JSON objects 
json_array = []
# Create a variable to have the max number of records
records_to_filter = 2000
count = 0


# Read data
with open('data-source/access.log', 'r') as file:
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
with open('output/result.json', 'w') as file:
    file.write(json_result)


df = pd.DataFrame(grouped)

# Calculate the z-score for request_count
df['request_count_zscore'] = zscore(df['request_count'])

# Define a threshold for anomalies (e.g., z-score greater than 3)
threshold = 3

# Identify anomalies
anomalies = df[df['request_count_zscore'] > threshold]

# Calculate the proportion of anomalies
proportion_anomalies = len(anomalies) / len(df)* 100

print("Proportion of anomalies found:", proportion_anomalies)

            
            