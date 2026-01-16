#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
dhis2_username = "*****"
dhis2_password = "*****"

from constants import LOG_FILE_PROGRAM_INDICATORS_POST, LOG_FILE_EVENT_ERROR_LOG

# DHIS2 API credentials and URL

DHIS2_API_GET_URL = "https://links.hispindia.org/nepalhmis/api/"
DHIS2_AUTH_GET = ("*****", "*****")

dhis2_username = "*****"
dhis2_password = "*****"

#DHIS2_API_POST_URL = "https://links.hispindia.org/nepal_climate/api/"
#DHIS2_API_POST_URL =  "https://links.hispindia.org/pmnp_pilot/api/"
DHIS2_API_POST_URL =  "https://tracker.hivaids.gov.np/save-child-2.27/api/"
#DHIS2_AUTH_POST = ("****", "*****")

DHIS2_AUTH_POST = ("*****", "*****")

#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_PROGRAM_INDICATORS_POST, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Program Indicators post start . { current_time_start }" )
logging.info(f"Program Indicators post start . { current_time_start }")

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


def push_program_indicator_in_dhis2(session_post, program_indicator_post_payload, pi_uid, pi_name, row ):
    #
    try:
        orgunit_post_url = f"{DHIS2_API_POST_URL}programIndicators"
        response = session_post.post(orgunit_post_url, data=json.dumps(program_indicator_post_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        print(f"Program Indicator created successfully for row : {row}, pi_uid : {pi_uid}, and pi_name: {pi_name}")
        logging.info(f"Program Indicator created successfully for row : {row}, pi_uid : {pi_uid}, and pi_name: {pi_name}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        
        print(f"Failed to create Program Indicator. for row : {row}. Error: {response.text}")
        logging.error(f"Failed to create Program Indicator for row : {row}. pi_uid : {pi_uid} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
program_indicators_import_excel_file_path = 'program_indicators_import.xlsx'

print( f"file_name . { program_indicators_import_excel_file_path }" )
logging.info(f"file_name . { program_indicators_import_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    # add dtype='object' for ready text start from 0
    program_indicator_list = pd.read_excel(program_indicators_import_excel_file_path, dtype='object')
    print( f"length of program_indicator_list. { len(program_indicator_list) }" )
    logging.info( f"length of program_indicator_list . { len(program_indicator_list) }" )
    for index, program_indicator_Row in program_indicator_list.iterrows():
        #print(f"Row {index + 1}: {orgunitRow}" )
        #print(f"Row {index + 1} " )
        #orgunit_response_data = get_orgunit_details( session_get, orgunitRow['orgunit_uid'] )

        analyticsPeriodBoundaries = []

        analyticsPeriodBoundaries.append({
            "id": program_indicator_Row['before_uid'],
            "boundaryTarget": program_indicator_Row['boundaryTarget'],
            "analyticsPeriodBoundaryType": program_indicator_Row['analyticsPeriodBoundaryType_before'],
        })

        analyticsPeriodBoundaries.append({
            "id": program_indicator_Row['after_uid'],
            "boundaryTarget": program_indicator_Row['boundaryTarget'],
            "analyticsPeriodBoundaryType": program_indicator_Row['analyticsPeriodBoundaryType_after'],
        })

        program_indicator_post_payload = {

            "id": program_indicator_Row['uid'],
            "name": program_indicator_Row['name'],
            "shortName": program_indicator_Row['shortName'],
            "program":{ "id" : program_indicator_Row['program']} ,
            "aggregationType": program_indicator_Row['aggregationType'],
            "analyticsType": program_indicator_Row['analyticsType'],
            "expression": program_indicator_Row['expression'],
            "filter": program_indicator_Row['filter'],
            "analyticsPeriodBoundaries" : analyticsPeriodBoundaries
           
        }

        if program_indicator_post_payload:
            #print( f"orgUnit_post_payload for post . { orgUnit_post_payload }" )
            executor.submit( push_program_indicator_in_dhis2, session_post, program_indicator_post_payload, program_indicator_Row['uid'], program_indicator_Row['name'], index+1 )
        
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Program Indicators post end . { current_time_end }" )
logging.info(f"Program Indicators post end . { current_time_end }")

