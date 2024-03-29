import re
import json
import pandas as pd
import sys
import os
from scipy.stats import zscore

file_route = ""
json_route = ""
records_to_filter = 0
anomalies_threshold = 0
bf_threshold = 0


def init_params():
    global file_route, json_route, records_to_filter, anomalies_threshold, bf_threshold
   
    file_route = sys.argv[1]  # First argument
    json_route = sys.argv[2]  # Second argument
    records_to_filter = int(sys.argv[3])  # Third argument
    anomalies_threshold = int(sys.argv[4])  # Fourth argument
    bf_threshold = int(sys.argv[5])  # Fifth argument
    
def check_params():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 6:
        print("We're looking for 6 parameters: file_route, records_to_filter, anomalies_threshold ,bf_threshold")
        sys.exit(1)

def check_input_file():
    # Check if the file exists
    if not os.path.isfile(file_route):
        print(f"Error: File '{file_route}' does not exist.")
        sys.exit(1)          

def check_int_parse():
# Check if records_to_filter, anomalies_threshold, and bf_threshold are integers
    try:
        int(records_to_filter)
        int(anomalies_threshold)
        int(bf_threshold)
    except ValueError:
        print("Error: records_to_filter, anomalies_threshold, and bf_threshold must be integers.")
        sys.exit(1)

def create_output_directory():
    # Create the output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
def read_and_filter_data():
    count = 0
    json_array = []
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
    # Creating a Dataframe and returning grouped data by IP address and HTTP method, count requests
    initial_dataframe = pd.DataFrame(json_array)
    print("Initial Dataframe after data clean:")
    print(initial_dataframe)
    filtered_data = initial_dataframe.groupby(['ip', 'method']).size().reset_index(name='request_count')  
    print("Requests by ip count results:")
    print(filtered_data)
    return filtered_data     

def build_output_json(df):
    # Convert the DataFrame to JSON format
    json_result = df.to_json(orient='records')
    # Write the JSON to a file
    with open(json_route, 'w') as file:
        file.write(json_result)
        
def calculate_anomalies(df):
    # Calculate the z-score for request_count
    df['request_count_zscore'] = zscore(df['request_count'])
    # Identify anomalies
    anomalies = df[df['request_count_zscore'] > anomalies_threshold]
    print("Print anomalies")
    print(anomalies)
    # Calculate the proportion of anomalies
    proportion_anomalies = len(anomalies) / len(df)* 100
    print("Proportion of anomalies found:", proportion_anomalies)
    return anomalies
    
def calculate_brute_force_attacks(df):    
    # Group DataFrame by IP address and sum the request counts
    ip_request_counts = df.groupby('ip')['request_count'].sum()
    # Identify potential brute force attacks
    potential_brute_force = ip_request_counts[ip_request_counts > bf_threshold]
    # Print IP addresses involved in potential brute force attacks
    if not potential_brute_force.empty:
        print("Potential Brute Force Attacks Results:")
        print(potential_brute_force)
    else:
        print("No potential brute force attacks detected.")

check_params()
init_params()
check_input_file()
check_int_parse()
create_output_directory()              
df = read_and_filter_data()
anomalies = calculate_anomalies(df)
build_output_json(anomalies)
calculate_brute_force_attacks(df)



            