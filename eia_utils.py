#-------------------------------------------------------------------------------------------------------------------------------------
# eia_utils.py
# Description:
#   This is a collection of utility functions to extract data from EIA that can be used by other code. 
# ------------------------------------------------------------------------------------------------------------------------------------


import pandas as pd
import requests
import json
import os
from datetime import datetime, timedelta
import pickle

# ------------------------------------------------------------------------------------------------------------------------------------
# get_state_electricity_capacity  
# Description:
#   Gets the electricity capacity data which is tagged by state, year, sector it belongs to, energy source used for generation. 
#  
# Input:
#   start_year (YYYY) (string) - This is optional. If not supplied, we will get the data starting from the earliest year for which it is 
#                       available
#   end_year (YYYY) (string) - This is optional. If not supplied, we will get the data up to the latest year for which it is available
# Output:
#   raw_data - A dataframe containing the raw data
# Note: 
#   EIA uses HTML basic auth. So you need to use this "API key", not as an API key, but as a username. 
# ------------------------------------------------------------------------------------------------------------------------------------
def get_state_electricity_capacity(start_year=None, end_year = None):
    url = "https://api.eia.gov/v2/electricity/state-electricity-profiles/capability/data/"
    parameters = {
                "frequency": "annual",
                "data[0]": "capability",
                "start": start_year,
                "end": end_year
                }

    username = os.getenv("EIA_API_KEY")   # You need to store your API key as a User Variable in Windows or store it in .bashrc 
    resp = requests.get(url, auth = (username, ""), params=parameters) # This is the API call to the EIA database
    raw_data = pd.DataFrame(json.loads(resp.text)['response']['data'])
    return(raw_data)

# ------------------------------------------------------------------------------------------------------------------------------------
# get_state_electricity_consumption  
# Description:
#   Gets the electricity consumption data which is tagged by state, month, sector it belongs to, energy source used for generation. 
#  
# Input:
#   start_year (YYYY-MM) (string) - This is optional. If not supplied, we will get the data starting from the earliest month and year  
#                                   for which it is available
#   end_year (YYYY-MM) (string) - This is optional. If not supplied, we will get the data up to the latest data avaialble
# Output:
#   raw_data - A dataframe containing the raw data
# ------------------------------------------------------------------------------------------------------------------------------------
def get_state_electricity_consumption(start_month=None, end_month = None):
    url = "https://api.eia.gov/v2/electricity/retail-sales/data/"
    parameters = {
                "frequency": "monthly",
                "data[0]": "sales",
                "start": start_month,
                "end": end_month
                }

    username = os.getenv("EIA_API_KEY")   # You need to store your API key as a User Variable in Windows or store it in .bashrc 
    resp = requests.get(url, auth = (username, ""), params=parameters) # This is the API call to the EIA database
    raw_data = pd.DataFrame(json.loads(resp.text)['response']['data'])
    return(raw_data)

