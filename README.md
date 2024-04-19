##Data Challenge

### Requirements:

- VSCode
- Python - Latest version
- Package Installer for Python [pip](https://pip.pypa.io/en/stable/installation/)
- Dependencies: `pip install pandas scipy`


### Configuration for Launching the Script (Using VSCode)

The launch.json file specifies the configuration settings for launching the script using Visual Studio Code's debugger, this file is already on the code:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Launch",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "args": [
                "data-source/access.log",
                "output/result.json",
                "1000",
                "3",
                "10"
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

## Goal

Source IPs that performed a (statistically) anomalous number of requests per HTTP method (This is using 1000 records and threshold of 3):

| ip            | method | request_count | request_count_zscore |
|---------------|--------|---------------|----------------------|
| 130.185.74.243 | GET    | 78            | 3.578874             |
| 31.56.96.51    | GET    | 72            | 3.264884             |
| 66.249.66.194 | GET    | 88            | 4.102190             |
| 66.249.66.91  | GET    | 83            | 3.840532             |

JSON:


```json
[
    {
        "ip": "130.185.74.243",
        "method": "GET",
        "request_count": 78,
        "request_count_zscore": 3.5788737444
    },
    {
        "ip": "31.56.96.51",
        "method": "GET",
        "request_count": 72,
        "request_count_zscore": 3.2648839696
    },
    {
        "ip": "66.249.66.194",
        "method": "GET",
        "request_count": 88,
        "request_count_zscore": 4.1021900358
    },
    {
        "ip": "66.249.66.91",
        "method": "GET",
        "request_count": 83,
        "request_count_zscore": 3.8405318901
    }
]

```

## Deliverables

- Implementation code in Python [here](https://github.com/natacardona/meli-data-test/blob/main/main.py)

## Written report detailing your:

- **Assumptions**: We can have a lot of assumptions here, but we're going to take an example and emit some conclusions:

    Based on this data:


    | ip            | method | request_count | request_count_zscore |
    |---------------|--------|---------------|----------------------|
    | 130.185.74.243 | GET    | 78            | 3.578874             |
    | 31.56.96.51    | GET    | 72            | 3.264884             |
    | 66.249.66.194 | GET    | 88            | 4.102190             |
    | 66.249.66.91  | GET    | 83            | 3.840532             |

    **High Request Counts**: IP addresses 130.185.74.243, 31.56.96.51, 66.249.66.194, and 66.249.66.91 have relatively high request counts compared to other IP addresses in the dataset. This may indicate that these IP addresses are making a large number of requests to the server.

    **Similar Request Methods**: All the IP addresses listed are using the HTTP method 'GET' for their requests. This suggests that these IP addresses are primarily fetching data from the server rather than submitting data or making other types of requests.

    **Z-score Analysis**: The request_count_zscore column provides z-scores for the request counts of each IP address. Z-scores measure how many standard deviations an element is from the mean. IP address 66.249.66.194 has the highest z-score (4.102190), indicating that its request count is more than four standard deviations above the mean. This IP address may be considered an outlier in terms of request count compared to the rest of the dataset.

    **Potential Anomalies**: IP addresses with high request counts and high z-scores may be considered potential anomalies or outliers in the dataset. These IP addresses could be investigated further to determine if their behavior is unusual or unexpected.

   **Patterns or Trends**: Analyzing patterns or trends in request counts over time for these IP addresses could provide insights into their behavior. For example, are there certain times of day when request counts are consistently high? Are there any sudden spikes or drops in request counts that may indicate unusual activity?

- **Comments**: 

    All the code is documented line by line.

- **Analysis / observations**: 

    Detailed on the next section.

- **Problems, and solutions you encountered while doing this challenge**.

| Problem                               | Solution                                                                                     |
|---------------------------------------|----------------------------------------------------------------------------------------------|
| File too heavy                        | We left some instructions to read the file locally.                                           |
| Too much data to process             | We put a param inside the run script to process less data.                                    |
| We didn’t have a defined threshold to know a good number of anomalies | We put a param inside the run script to customize the anomalies, this is also attached to the way to improve the false positive and the false negatives. |
| We didn’t have a defined force brute threshold to filter the expected values | We put a param inside the run script to customize the force brute attacks inside the code. |

## Written report with the answers to the following questions:

#### What was the proportion of anomalies found?

This will be depend of the threshold assigned on the code execution, for example, I will put some results using:

`threshold = 3 and 1000 rows
Proportion of anomalies found: 3.8834951456310676 %`

`threshold = 4 and 1000 rows
Proportion of anomalies found: 0.9708737864077669`

`threshold = 5 and 1000 rows
Proportion of anomalies found: 0.0`

#### How would you change the method to produce less false positives?

Increase the threshold for anomalies detection. By setting a higher threshold, you're requiring a stronger deviation from the norm to be classified as an anomaly, which can reduce false positives. However, be cautious not to set it too high, as this might lead to missing genuine anomalies (increasing false negatives).


#### How would you change the method to produce less false negatives?

Decrease the threshold slightly to capture more anomalies without significantly increasing false positives. This adjustment allows for a more sensitive detection of anomalies, reducing false negatives at the expense of potentially introducing more false positives.

#### Considering only the features already included in the dataset, how would identify a brute force attack

Since there's a threshold value defined in the code as `bf_threshold`. This threshold represents the minimum number of requests that need to be made from an IP address for it to be considered a potential brute force attack. In this case our code, filter this data and build a result dataframe with the possible brute force attacks, and can be customized modifying the `bf_threshold` before to launch the project:

```python
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
```
