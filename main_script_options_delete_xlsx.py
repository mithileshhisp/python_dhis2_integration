#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
import os
dhis2_username = "hispdev"
dhis2_password = "Devhisp@1"

from constants import LOG_FILE_OPTIONS_DELETE

# DHIS2 API credentials and URL

DHIS2_API_GET_URL = "******/api/"
DHIS2_AUTH_GET = ("*****", "******")

DHIS2_API_POST_URL =  "*********/api/"

DHIS2_AUTH_POST = ("*****", "******")

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log filename
#log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = LOG_FILE_OPTIONS_DELETE
#log_filename = f"{LOG_FILE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(filename=LOG_FILE_OPTIONS_DELETE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"options delete start . { current_time_start }" )
logging.info(f"options delete start . { current_time_start }")

tei_data_cache = {}
events_by_reg_id = {}

def assign_value_if_not_null(value):
    if value is not None and value != "null":
        return value
    elif value.isna():
            return ""
    else:
        return ""

def assign_value_if_NaN(value):
    if pd.notnull(value):
        return value
    else:
        return ""


def delete_options_in_dhis2(session_post, option_uid, row ):
    #
    try:
        option_post_url = f"{DHIS2_API_POST_URL}options/{option_uid}"
        response = session_post.delete(option_post_url, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        print(f"Option deleted successfully for row : {row}, option_uid : {option_uid}")
        logging.info(f"Option deleted successfully for row : {row}, option_uid : {option_uid}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        
        print(f"Failed to delete Option. for row : {row}. Error: {response.text}")
        logging.error(f"Failed to delete Option for row : {row}. option_uid : {option_uid} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
option_delete_excel_file_path = 'optionsDelete.xlsx'

print( f"file_name . { option_delete_excel_file_path }" )
logging.info(f"file_name . { option_delete_excel_file_path }")


with ThreadPoolExecutor(max_workers=20) as executor:
    # Create a session object for persistent connection
    # add dtype='object' for ready text start from 0
    options_list = pd.read_excel(option_delete_excel_file_path, dtype='object')
    print( f"length of options_list. { len(options_list) }" )
    logging.info( f"length of options_list . { len(options_list) }" )
    for index, optionRow in options_list.iterrows():
        #print(f"Row {index + 1}: {optionRow}" )
        #print(f"Row {index + 1} " )
        #option_response_data = get_option_details( session_get, optionRow['option_uid'] )

        option_uid =  assign_value_if_NaN(optionRow['uid'])
        
        if option_uid:
            #print( f"option_uid . { option_uid }" )
            executor.submit( delete_options_in_dhis2, session_post, option_uid, index+1 )
        
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"options delete end . { current_time_end }" )
logging.info(f"options delete end . { current_time_end }")

