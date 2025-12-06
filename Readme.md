# NGED DSO Datasets Downloader


This Python script is designed to automate the process of navigating the National Grid Electricity Distribution (NGED) curtailment analysis website, identifying available data, and downloading all associated CSV files into a structured local directory. It also creates a JSON file logging all downloaded datasets and their original source URLs.

<br></br>

## Prerequisites

Before running the script, ensure you have Python installed and the necessary libraries: `requests`, `beautifulsoup4 (bs4)`, and `lxml`.


You can install the dependencies using pip:

- bash
     - `pip install requests beautifulsoup4 lxml`


## How to Run the Script
**Save the code**: Save the provided Python code into a file (e.g., nged_dso_data.py).
**Execute**: Run the script from your terminal:
 - bash
    - `python nged_dso_data.py`


## Functionality
When executed, the script performs the following actions:
 - **Creates Root Directory**: A main folder named NGED_DSO_Datasets is created in the same directory where the script is run.
 - **Scrapes Data Page Links**: It visits the main [curtailment analysis page](https://dso.nationalgrid.co.uk/curtailment-analysis) and finds links to individual dataset pages.
 - **Downloads CSVs**:
     - It iterates through each dataset page found.
     - For each page, it creates a dedicated subfolder within NGED_DSO_Datasets (e.g., NGED_DSO_Datasets/April_2024_Data).
     - It identifies all CSV links on that page and downloads the files into the corresponding subfolder.

 - **Generates Log File**: A file named Dataset.json is created in the script's root directory. This file contains a JSON array detailing every downloaded CSV file, mapping a generated unique key (Page_Name__filename) to its full original URL.


## Project Structure After Running
After successful execution, your directory structure will look similar to this:
```python
.
├── download_data.py
├── Dataset.json
└── NGED_DSO_Datasets
    ├── April_2024_Data
    │   ├── Demand-curtailment-daily-MI-april-2024.csv
    │   └── Demand-curtailment-MI-report-april-2024.csv
    ├── March_2024_Data
    │   ├── Demand-curtailment-daily-MI-march-2024.csv
    │   └── Demand-curtailment-MI-report-march-2024.csv
    └── ... (more months/pages)
```


### Notes
**SSL Warnings**: The script includes code to ignore SSL verification warnings (warnings.simplefilter('ignore')) and uses verify=False in requests.get() calls. This is often necessary when dealing with certain institutional websites. Use this approach with caution in production environments.
**Dependencies**: The script relies on the HTML structure of the target website remaining consistent. If National Grid updates their website layout or class names, the selectors (e.g., `"button.button--primary.button--contextual"`, `"a[href$='.csv']"`) may need adjustment.