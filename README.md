# meli-data-test
# Anomaly Detection with Z-Scores

## Introduction

This project aims to detect anomalies in a dataset containing user actions on an e-commerce web application. The code provided calculates anomalies based on z-scores and identifies statistically anomalous IP addresses with a high number of requests per HTTP method.

## Installation

To run this project, make sure you have Python installed. You also need to install the following dependencies:
```bash
pip install pandas scipy
```
## Usage
To run the code, follow these steps:

Create a directory named data-source at the root of the project.
Copy the access.log file into the data-source directory.
Run the main script:
```bash
python main.py
```
## Explanation of the Approach
The main script main.py reads the data from the access.log file, processes it to identify the number of requests per IP address and HTTP method, calculates z-scores for the request counts, and identifies anomalies based on a predefined threshold.


## File Structure
.
├── data-source/
│   └── access.log
├── output/
│   └── result.json
├── main.py
└── README.md


## Additional Notes
The code assumes that the access.log file follows a specific format. Make sure the log file is formatted correctly for accurate results.
Adjust the threshold for anomalies as needed based on the characteristics of your dataset.
vbnet
