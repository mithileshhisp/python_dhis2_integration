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

from constants import LOG_FILE_ORGUNIT_UPDATE

# DHIS2 API credentials and URL

DHIS2_API_GET_URL =  "*******/api/"
DHIS2_AUTH_GET = ("*****", "*****")


#DHIS2_API_POST_URL =  "*********/api/"
#DHIS2_AUTH_POST = ("*****", "*****")


# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET
#session = requests.Session()
#session.auth = (USERNAME, PASSWORD)
session_get.headers.update({"Content-Type": "application/json"})

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
print( f"OrganisationUnits Meta Attribute value update start . { current_time_start }" )
logging.info(f"OrganisationUnits Meta Attribute value update start . { current_time_start }")


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

def update_orgunit_in_dhis2(session_get, orgUnit_update_payload, orgunit_uid, attribute_value, row ):
    #
    try:
        orgunit_post_url = f"{DHIS2_API_GET_URL}organisationUnits/{orgunit_uid}"
        response = session_get.put(orgunit_post_url, data=json.dumps(orgUnit_update_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        print(f"Orgunit update successfully for row : {row}, orgunit_uid : {orgunit_uid}, with attribute value : {attribute_value} at hierarchylevel: {orgUnit_update_payload.get('level')}")
        logging.info(f"Orgunit update successfully for row : {row}, orgunit_uid : {orgunit_uid}, with attribute value : {attribute_value} at hierarchylevel: {orgUnit_update_payload.get('level')}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        
        print(f"Failed to update Orgunit. for row : {row}. Error: {response.text}")
        logging.error(f"Failed to update Orgunit for row : {row}. orgunit_uid : {orgunit_uid} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
#orgunit_to_orgunit_post_excel_file_path = 'orgunit_to_orgunit_post.xlsx'
orgUnit_meta_attribute_value_update_excel_file_path = 'orgUnitMetaAttributeValueUpdate.xlsx'

print( f"file_name . { orgUnit_meta_attribute_value_update_excel_file_path }" )
logging.info(f"file_name . { orgUnit_meta_attribute_value_update_excel_file_path }")

with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    orgunit_list = pd.read_excel(orgUnit_meta_attribute_value_update_excel_file_path)

    #file_path = "input.xlsx"
    #sheet_name = "orgUnitAttributeValueUpdate"
    #df = pd.read_excel(file_path, sheet_name=sheet_name)

    print( f"length of orgunit_list. { len(orgunit_list) }" )
    logging.info( f"length of orgunit_list . { len(orgunit_list) }" )
    import_count = 1
    for index, orgunitRow in orgunit_list.iterrows():
        #print(f"Row {index + 1}: {orgunitRow}" )
        #print(f"Row {index + 1} " )
        import_count += 1
        org_uid = orgunitRow["uid"]
        attribute = orgunitRow["attribute"]
        attribute_value = orgunitRow["attributeValue"]

        orgunit_response_data_source = get_orgunit_details(DHIS2_API_GET_URL, session_get, org_uid )

        if orgunit_response_data_source:
            #orgunit_payload = orgunit_response_data
            
            updateOrgUnit = orgunit_response_data_source

            tempAttributeValues = [
                {
                    "value": attribute_value,
                    "attribute": {
                        "id": attribute
                    }
                }
            ]

            updateOrgUnit["attributeValues"] = tempAttributeValues
             #print(orgUnit_post_payload)
            executor.submit( update_orgunit_in_dhis2, session_get, updateOrgUnit, org_uid, attribute_value, index+1 )

if import_count == len(orgunit_list) + 1:
    print("update complete")

current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"OrganisationUnits Meta Attribute value update end . { current_time_end }" )
logging.info(f"OrganisationUnits Meta Attribute value update end . { current_time_end }")


'''
# CONFIG
DHIS2_BASE_URL = "https://your-dhis2-url/api/"
USERNAME = "username"
PASSWORD = "password"

# READ EXCEL
file_path = "input.xlsx"
sheet_name = "orgUnitAttributeValueUpdate"

df = pd.read_excel(file_path, sheet_name=sheet_name)

import_count = 1

for index, row in df.iterrows():
    import_count += 1
    uid = row["uid"]
    attribute = row["attribute"]
    attribute_value = row["attributeValue"]

    try:
        # GET organisationUnit
        get_url = f"{DHIS2_BASE_URL}organisationUnits/{uid}.json?paging=false"
        response = session.get(get_url)
        response.raise_for_status()

        orgUnitResponse = response.json()

        updateOrgUnit = orgUnitResponse

        tempAttributeValues = [
            {
                "value": attribute_value,
                "attribute": {
                    "id": attribute
                }
            }
        ]

        updateOrgUnit["attributeValues"] = tempAttributeValues

        # PUT update
        put_url = f"{DHIS2_BASE_URL}organisationUnits/{uid}"
        put_response = session.put(put_url, data=json.dumps(updateOrgUnit))

        if put_response.status_code in [200, 201]:
            print(f"Row - {import_count} update done response: {put_response.text}")
        else:
            print(f"Row - {import_count} error response: {put_response.text}")

    except Exception as e:
        print(f"{uid} -- Error!: {str(e)}")

if import_count == len(df) + 1:
    print("update complete")

'''