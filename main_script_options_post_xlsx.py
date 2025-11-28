#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
dhis2_username = "****"
dhis2_password = "******"

from constants import LOG_FILE_OPTIONS_POST, LOG_FILE_EVENT_ERROR_LOG

# DHIS2 API credentials and URL

DHIS2_API_GET_URL = "****/api/"
DHIS2_AUTH_GET = ("*****", "*****")


DHIS2_API_POST_URL = "****/api/"
DHIS2_AUTH_POST = ("****", "*****")
# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_OPTIONS_POST, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"optionSet options post start . { current_time_start }" )
logging.info(f"optionSet options post start . { current_time_start }")

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


def push_options_in_dhis2(session_post, optionSet_options_post_payload, option_uid, option_name, row ):
    #
    try:
        option_post_url = f"{DHIS2_API_POST_URL}options"
        response = session_post.post(option_post_url, data=json.dumps(optionSet_options_post_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        print(f"Option created successfully for row : {row}, option_uid : {option_uid}, and orgunit_name: {option_name}")
        logging.info(f"Option created successfully for row : {row}, option_uid : {option_uid}, and orgunit_name: {option_name}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        
        print(f"Failed to create Option. for row : {row}. Error: {response.text}")
        logging.error(f"Failed to create Option for row : {row}. option_uid : {option_uid} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
option_post_excel_file_path = 'optionSetOptionsPost.xlsx'

print( f"file_name . { option_post_excel_file_path }" )
logging.info(f"file_name . { option_post_excel_file_path }")


with ThreadPoolExecutor(max_workers=20) as executor:
    # Create a session object for persistent connection
    # add dtype='object' for ready text start from 0
    options_list = pd.read_excel(option_post_excel_file_path, dtype='object')
    print( f"length of options_list. { len(options_list) }" )
    logging.info( f"length of options_list . { len(options_list) }" )
    for index, optionRow in options_list.iterrows():
        #print(f"Row {index + 1}: {orgunitRow}" )
        #print(f"Row {index + 1} " )
        #orgunit_response_data = get_orgunit_details( session_get, orgunitRow['orgunit_uid'] )

        optionSet_options_post_payload = {
            "id": assign_value_if_NaN(optionRow['uid']),
            "name": assign_value_if_NaN(optionRow['name']),
            "code": assign_value_if_NaN(optionRow['code']),
            "optionSet": { "id" :  assign_value_if_NaN(optionRow['optionSet'])},
            "sortOrder": assign_value_if_NaN(optionRow['sortOrder'])
        }

        if optionSet_options_post_payload:
            #print( f"optionSet_options_post_payload for post . { optionSet_options_post_payload }" )
            executor.submit( push_options_in_dhis2, session_post, optionSet_options_post_payload, optionRow['uid'], optionRow['name'], index+1 )
        
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"optionSet options post end . { current_time_end }" )
logging.info(f"optionSet options post end . { current_time_end }")

