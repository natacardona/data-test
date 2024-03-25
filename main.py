# Importing regular expression python module
import re
# Read data
with open('data-source/access.log', 'r') as file:
    # Read each line of the file
    for line in file:
        # Regular expression pattern to extract relevant data
        pattern = r'(\S+) - - \[([\w:/]+\s[+\-]\d{4})\] "(GET|POST|PUT|DELETE|PATCH) (.+?)" (\d+)'
        # Finding all possible matches using regular expression
        matches = re.findall(pattern, line)
        # Printing
        for match in matches:
            # Collecting the results
            ip,timestamp, method, request, status = match
            # Printing the results
            print("IP:", ip)
            print("Timestamp")
            print("Method:", method)
            print("Request:", request)
            print("Status:", status)
            print("-----------------")

