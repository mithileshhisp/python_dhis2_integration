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

from constants import LOG_FILE_ORGUNIT_UPDATE

# DHIS2 API credentials and URL


DHIS2_API_GET_URL =  "******/events/api/"
DHIS2_AUTH_GET = ("******", "******")

DHIS2_API_POST_URL =  "******/events/api/"
DHIS2_AUTH_POST = ("*******", "********")



# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log filename
#log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = LOG_FILE_ORGUNIT_UPDATE
#log_filename = f"{LOG_FILE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"organisationUnits to organisationUnits name update start . { current_time_start }" )
logging.info(f"organisationUnits to organisationUnits name update start . { current_time_start }")

tei_data_cache = {}
events_by_reg_id = {}

#excel_path = 'hwc_event_data.xlsx' 
#data_dict = read_excel_to_dict(excel_path)
'''
import pandas as pd
file_path = 'read_sample.xlsx'
data = pd.read_excel(file_path)
columns_of_interest = ['Column1', 'Column2', 'Column3', 'Column4']
data_of_interest = data[columns_of_interest]
for index, row in data_of_interest.iterrows():
    print(f"Row {index + 1}:")
    for col in columns_of_interest:
        print(f"  {col}: {row[col]}")
    print()
'''

def get_orgunit_details( org_unit_url, session_get,orgunit_uid):
    
    #https://ln4.hispindia.org/timor_dev/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
   
    #https://links.hispindia.org/nepalhmis/api/organisationUnits/cCTQiGkKcTk.json
    #event_search_url = f"{event_push_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={programID}&status=ACTIVE&skipPaging=true&filter={event_search_dataElement_uid}:eq:{BenCallID}"
    orgunit_get_url = f"{org_unit_url}organisationUnits/{orgunit_uid}.json?fields=*"

    #print(event_search_url)
    #print(f" orgunit_get_url : {orgunit_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session_get.get(orgunit_get_url)
    
    if response.status_code == 200:
        orgunit_response_data = response.json()
        #print(response)
        #print(orgunit_response_data)
        return orgunit_response_data 
    else:
        return []

def update_orgunit_in_dhis2(session_post, orgUnit_update_payload, orgunit_uid, row ):
    #
    try:
        orgunit_post_url = f"{DHIS2_API_POST_URL}organisationUnits/{orgunit_uid}"
        response = session_post.put(orgunit_post_url, data=json.dumps(orgUnit_update_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        print(f"Orgunit update successfully for row : {row}, orgunit_uid : {orgunit_uid}, at hierarchylevel: {orgUnit_update_payload.get('level')}")
        logging.info(f"Orgunit update successfully for row : {row}, orgunit_uid : {orgunit_uid}, at hierarchylevel: {orgUnit_update_payload.get('level')}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        
        print(f"Failed to update Orgunit. for row : {row}. Error: {response.text}")
        logging.error(f"Failed to update Orgunit for row : {row}. orgunit_uid : {orgunit_uid} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
#orgunit_to_orgunit_post_excel_file_path = 'orgunit_to_orgunit_post.xlsx'
orgunit_to_orgunit_post_excel_file_path = 'orgunit_to_orgunit_name_update.xlsx'

print( f"file_name . { orgunit_to_orgunit_post_excel_file_path }" )
logging.info(f"file_name . { orgunit_to_orgunit_post_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    orgunit_list = pd.read_excel(orgunit_to_orgunit_post_excel_file_path)
    print( f"length of orgunit_list. { len(orgunit_list) }" )
    logging.info( f"length of orgunit_list . { len(orgunit_list) }" )
    for index, orgunitRow in orgunit_list.iterrows():
        #print(f"Row {index + 1}: {orgunitRow}" )
        #print(f"Row {index + 1} " )
        orgunit_response_data_source = get_orgunit_details(DHIS2_API_GET_URL, session_get, orgunitRow['orgunit_uid'] )

        if orgunit_response_data_source:
            #orgunit_payload = orgunit_response_data
            
            orgunit_response_data_update = get_orgunit_details( DHIS2_API_POST_URL, session_post, orgunitRow['orgunit_uid'] )
            
            if orgunit_response_data_update:
                
                '''
                orgUnit_update_payload = {
                    "name": orgunit_response_data_source.get("name"),
                    "shortName": orgunit_response_data_source.get("shortName")
                }
                '''
                
                orgUnit_update_payload = orgunit_response_data_update.copy()
                orgUnit_update_payload["name"] = orgunit_response_data_source.get('name')
                orgUnit_update_payload["shortName"] = orgunit_response_data_source.get('shortName')
               
                #print(orgUnit_post_payload)
                executor.submit( update_orgunit_in_dhis2, session_post, orgUnit_update_payload, orgunitRow['orgunit_uid'], index+1 )
            
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"organisationUnits to organisationUnits name update end . { current_time_end }" )
logging.info(f"organisationUnits to organisationUnits name update end . { current_time_end }")

