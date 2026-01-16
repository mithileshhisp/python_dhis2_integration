#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member,get_option_details_test
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
dhis2_username = "*****"
dhis2_password = "*****"

from constants import LOG_FILE_OPTIONS_TRANSLATION_POST

# DHIS2 API credentials and URL

DHIS2_API_GET_URL = "https://links.hispindia.org/nepalhmis/api/"
DHIS2_AUTH_GET = ("****", "****")

dhis2_username = "*****"
dhis2_password = "*****"

#DHIS2_API_POST_URL = "https://links.hispindia.org/nepal_climate/api/"
#DHIS2_API_POST_URL =  "https://hmistraining.mm.dhis2.net/train/api/"
DHIS2_API_POST_URL =  "https://mbdr.mm.dhis2.net/dhis/api/"

DHIS2_AUTH_POST = ("******", "*****")
#DHIS2_AUTH_POST = ("******", "*****")

#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_OPTIONS_TRANSLATION_POST, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"options translations post start . { current_time_start }" )
logging.info(f"options translations post start . { current_time_start }")

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

def get_option_details(session_post,option_uid):
    
    option_get_url = f"{DHIS2_API_POST_URL}options/{option_uid}.json"

    #print(option_grp_get_url)
    #print(f" event_search_url : {event_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session_post.get(option_get_url)
    
    if response.status_code == 200:
        option_response_data = response.json()
        #print(response)
        #print(option_grp_response_data)
        return option_response_data 
    else:
        return []
    

def push_options_translation_in_dhis2(session_post, option_response_data, option_uid, translation,row ):
    #
    try:
        option_post_url = f"{DHIS2_API_POST_URL}options/{option_uid}"
        response = session_post.put(option_post_url, data=json.dumps(option_response_data), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        print(f"Option translation update successfully for row : {row}, option_uid : {option_uid}, and option_translation: {translation}")
        logging.info(f"Option translation update successfully for row : {row}, option_uid : {option_uid}, and option_translation: {translation}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        
        print(f"Failed to update Option translation . for row : {row}. Error: {response.text}")
        logging.error(f"Failed to update Option translation for row : {row}. option_uid : {option_uid} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
option_translation_excel_file_path = 'optionTranslationUpdate.xlsx'

print( f"file_name . { option_translation_excel_file_path }" )
logging.info(f"file_name . { option_translation_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    # add dtype='object' for ready text start from 0
    options_list = pd.read_excel(option_translation_excel_file_path, dtype='object')
    print( f"length of options_list. { len(options_list) }" )
    logging.info( f"length of options_list . { len(options_list) }" )
    for index, optionRow in options_list.iterrows():
        #print(f"Row {index + 1}: {optionRow}" )
        #print(f"Row {index + 1} " )
        option_response_data = get_option_details( session_post, optionRow['uid'] )

        if option_response_data:
            translations = []
            translations.append({
                "property": optionRow["property"],
                "locale": optionRow["locale"],
                "value": optionRow["value"]
            })
             
            option_response_data["translations"] = translations

            #print( f"option_response_data . { option_response_data }" )
            #logging.info(f"event_payload . { option_group_response_data }")
            #executor.submit( push_events_in_dhis2, session, event_payload, eventUid, index+1 )
            executor.submit( push_options_translation_in_dhis2, session_post, option_response_data, optionRow['uid'], optionRow['value'], index+1 )

        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"options translations post end . { current_time_end }" )
logging.info(f"options translations post end . { current_time_end }")

