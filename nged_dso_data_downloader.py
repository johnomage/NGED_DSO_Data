
"""
This Python script is designed to automate the process of navigating the National Grid Electricity Distribution (NGED)
curtailment analysis website, identifying available data, and downloading all associated CSV files into a structured
local directory. It also creates a JSON file logging all downloaded datasets and their original source URLs.
"""

# import packages
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json
import warnings
warnings.simplefilter('ignore')


BASE_URL = "https://dso.nationalgrid.co.uk/curtailment-analysis"
BASE_RESPONSE = requests.get(BASE_URL, verify=False)

# prepare base soup
soup = BeautifulSoup(BASE_RESPONSE.text, 'lxml' )

links_to_data_page_dict = {Path(link['href']).stem.title().replace('-', '_'): # key - Input data page name
                      link['href']                                           # value - Input data url
                      for link in soup.find_all('a', class_="button button--primary button--contextual")
                    }


page_name_list = [] # this list holds all CSVs

# Make root folder if it doesn't exist
ROOT_DIR = Path("NGED_DSO_Datasets")
ROOT_DIR.mkdir(exist_ok=True)

# Iterate through each data page in links_to_data_page_dict
for page_name, page_link in links_to_data_page_dict.items():
    page_html_file = requests.get(page_link, verify=False).text # Fetch the HTML content of the current data page
    page_soup = BeautifulSoup(page_html_file, 'lxml') # prepare the delicious html soup
    
    # Select all 'a' tags whose 'href' ends with '.csv' and create a dictionary
    # The dictionary maps a unique key (page_name__filename) to the full CSV URL
    csv_links_dict = {f"{page_name}__{Path(tag['href']).stem}": tag['href'] for tag in page_soup.select("a[href$='.csv']")} # 

    page_name_list.append(csv_links_dict)
    
    # create a subfolder for the current page's downloads within the root directory
    # each file goes to it's own source page name
    page_folder = ROOT_DIR.joinpath(Path(page_name))
    page_folder.mkdir(exist_ok=True)

    # now download each csv file into it's folder
    for file in csv_links_dict.values():
        save_path = page_folder / Path(file).name # make a path to the file for saving
        content = requests.get(file, verify=False).content 

        with open(save_path, 'wb') as f:
           f.write(content) 

# now log all csv details
with open('Dataset.json', 'w') as f:
    f.write(json.dumps(page_name_list))


