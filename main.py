# Importing regular expression python module
import re
import json
import pandas as pd


 # Create an empty list to store JSON objects 
json_array = []
# Create a variable to have the max number of records
records_to_filter = 100
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


            
            