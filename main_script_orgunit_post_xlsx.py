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
dhis2_password = "*****"

from constants import LOG_FILE_ORGUNIT_POST, LOG_FILE_EVENT_ERROR_LOG

# DHIS2 API credentials and URL
DHIS2_API_GET_URL = "****/api/"
DHIS2_AUTH_GET = ("*****", "*****")


DHIS2_API_POST_URL = "****/api/"
DHIS2_AUTH_POST = ("****", "*****")

#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_ORGUNIT_POST, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"organisationUnits post start . { current_time_start }" )
logging.info(f"organisationUnits post start . { current_time_start }")

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

def get_orgunit_details(session_get,orgunit_uid):
    
    #https://ln4.hispindia.org/timor_dev/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
   
    #https://links.hispindia.org/nepalhmis/api/organisationUnits/cCTQiGkKcTk.json
    #event_search_url = f"{event_push_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={programID}&status=ACTIVE&skipPaging=true&filter={event_search_dataElement_uid}:eq:{BenCallID}"
    orgunit_get_url = f"{DHIS2_API_GET_URL}organisationUnits/{orgunit_uid}.json"

    #print(event_search_url)
    #print(f" event_search_url : {event_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session_get.get(orgunit_get_url)
    
    if response.status_code == 200:
        orgunit_response_data = response.json()
        #print(response)
        #print(orgunit_response_data)
        return orgunit_response_data 
    else:
        return []

def push_orgunit_in_dhis2(session_post, orgunit_payload, orgunit_uid, orgunit_name, row ):
    #
    try:
        orgunit_post_url = f"{DHIS2_API_POST_URL}organisationUnits"
        response = session_post.post(orgunit_post_url, data=json.dumps(orgunit_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        print(f"Orgunit created successfully for row : {row}, orgunit_uid : {orgunit_uid}, and orgunit_name: {orgunit_name}")
        logging.info(f"Orgunit created successfully for row : {row}, orgunit_uid : {orgunit_uid}, and orgunit_name: {orgunit_name}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        
        print(f"Failed to create Orgunit. for row : {row}. Error: {response.text}")
        logging.error(f"Failed to create Orgunit for row : {row}. orgunit_uid : {orgunit_uid} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
orgunit_post_excel_file_path = 'orgUnitPost.xlsx'

print( f"file_name . { orgunit_post_excel_file_path }" )
logging.info(f"file_name . { orgunit_post_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    # add dtype='object' for ready text start from 0
    orgunit_list = pd.read_excel(orgunit_post_excel_file_path, dtype='object')
    print( f"length of orgunit_list. { len(orgunit_list) }" )
    logging.info( f"length of orgunit_list . { len(orgunit_list) }" )
    for index, orgunitRow in orgunit_list.iterrows():
        #print(f"Row {index + 1}: {orgunitRow}" )
        #print(f"Row {index + 1} " )
        #orgunit_response_data = get_orgunit_details( session_get, orgunitRow['orgunit_uid'] )

        orgUnit_post_payload = {
            "id": assign_value_if_NaN(orgunitRow['uid']),
            "name": assign_value_if_NaN(orgunitRow['name']),
            "shortName": assign_value_if_NaN(orgunitRow['shortName']),
            "parent":{ "id" : assign_value_if_NaN(orgunitRow['parent'])} ,
            "code": assign_value_if_NaN(orgunitRow['code']),
            "comment": assign_value_if_NaN(orgunitRow['comment']),
            "description": assign_value_if_NaN(orgunitRow['description']),
            "level": assign_value_if_NaN(orgunitRow['level']),
            "phoneNumber": assign_value_if_NaN(orgunitRow['phoneNumber']),
            "email": assign_value_if_NaN(orgunitRow['email']),
            "address": assign_value_if_NaN(orgunitRow['address']),
            "contactPerson": assign_value_if_NaN(orgunitRow['contactPerson']),
            "openingDate": assign_value_if_NaN(orgunitRow['openingDate'])
        }

        if orgUnit_post_payload:
            #print( f"orgUnit_post_payload for post . { orgUnit_post_payload }" )
            executor.submit( push_orgunit_in_dhis2, session_post, orgUnit_post_payload, orgunitRow['uid'], orgunitRow['name'], index+1 )
        
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"organisationUnits post end . { current_time_end }" )
logging.info(f"organisationUnits post end . { current_time_end }")

