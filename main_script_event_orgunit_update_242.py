#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth

from constants import LOG_FILE_EVENT_ORGUNIT_UPDATE, LOG_FILE_EVENT_ERROR_LOG

# DHIS2 API credentials and URL

#https://mbdr.moh.gov.mm/dhis/api/tracker/events/bo9EnvkjuZ8.json
DHIS2_API_POST_URL = "******/dhis/api/tracker/" # for 2.42
DHIS2_AUTH_POST = ("******", "******")

DHIS2_API_GET_URL = "*****/dhis/api/tracker" # for 2.42
DHIS2_AUTH_GET = ("******", "*******")


# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_EVENT_ORGUNIT_UPDATE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"event orgUnit update start . { current_time_start }" )
logging.info(f"event orgUnit update start . { current_time_start }")

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

def get_event_details(session_get,event_uid):
    
    #https://ln4.hispindia.org/timor_dev/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
   
    #event_search_url = f"{event_push_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={programID}&status=ACTIVE&skipPaging=true&filter={event_search_dataElement_uid}:eq:{BenCallID}"
    event_get_url = f"{DHIS2_API_GET_URL}/events/{event_uid}.json"

    #print(event_search_url)
    #print(f" event_get_url : {event_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session_get.get(event_get_url)
    
    if response.status_code == 200:
        event_response_data = response.json()
        #print(response)
        #print(event_response_data)
       
        #print(f"event_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
        dataValues = event_response_data.get('dataValues',[])
        #events = event_response_data.get('response', {})
        #print(f" dataValues : {dataValues}" )
        return event_response_data 
    else:
        return []



def update_event_orgunit_in_dhis2_242_xlsx(session, event_update_orgunit_payload, eventUID, event_orgunit, row_no):
    #
    try:
        #print(json.dumps(event_update_orgunit_payload, indent=2))
        url = f"{DHIS2_API_GET_URL}?async=false&importStrategy=UPDATE"
        #print(f" event_update_url : {url}" )
        #https://mbdr.moh.gov.mm/dhis/api/42/tracker?async=false&importStrategy=DELETE
        response = session.post(
            url,
            json=event_update_orgunit_payload,
            headers={"Content-Type": "application/json"}
        )

        #print("HTTP Status:", response.status_code)
        #print(response.text)
        resp = response.json()

        status = resp.get("status")
        event_report = (
        resp.get("bundleReport", {})
            .get("typeReportMap", {})
            .get("EVENT", {})
        )

        event_stats = event_report.get("stats", {})

        updated = event_stats.get("updated", 0)
        created = event_stats.get("created", 0)
        ignored = event_stats.get("ignored", 0)
        deleted = event_stats.get("deleted", 0)
        total = event_stats.get("total", 0)

        #print(f"Ignored: {ignored}")
        #print(f"Updated: {updated}")
        #print(f"Created: {created}")
        #print(f"status: {status}")

        object_reports = event_report.get("objectReports", [])
        for obj in object_reports:
            #print(f"Event UID: {obj.get('uid')}")
            updated_event_uid = obj.get('uid')

        #resp = response.json()
        
        event_report = (
            resp.get("bundleReport", {})
                .get("typeReportMap", {})
                .get("EVENT", {})
        )

        #resp = response.json()
        '''
        status = resp.get("status")
        updated = resp.get("stats", {}).get("updated", 0)
        created = resp.get("stats", {}).get("created", 0)
        ignored = resp.get("stats", {}).get("ignored", 0)
        deleted = resp.get("stats", {}).get("deleted", 0)
        total = resp.get("stats", {}).get("total", 0)

        print(f"Status: {status}")
        print(f"Updated: {updated}")
        print(f"deleted: {deleted}")
        print(f"total: {total}")

        '''
        #print(event_report)
        #print(f" event_report : {event_report}" )
        
        print(f"Events updated successfully. Row No: {row_no}.updated event: {updated_event_uid}.with event_orgunit {event_orgunit} created:{created}. updated:{updated}. ignored:{ignored}")
        logging.info(f"Events updated successfully. Row No : {row_no}. updated event : {updated_event_uid}. with event_orgunit {event_orgunit} created : {created} .updated : {updated} .ignored : {ignored}")

    except requests.RequestException as e:
        
        print(f"Failed to update events. Error: {event_report}")
        logging.error(f"Failed to update events. Row No : {row_no} .Error : {event_report} .Status code: {response.status_code} .error details: {response.json()} .Error: {response.text}")


event_orgunit_update_excel_file_path = 'eventOrgUniyUpdate.xlsx'

print( f"file_name . { event_orgunit_update_excel_file_path }" )
logging.info(f"file_name . { event_orgunit_update_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    event_list = pd.read_excel(event_orgunit_update_excel_file_path)
    print( f"event count . { len(event_list) }" )
    logging.info(f"event count . { len(event_list) }")
    for index, eventRow in event_list.iterrows():
        #print(f"Row {index + 1}: {eventRow}" )
        #print(f"Row {index + 1} " )
        event_response_data = get_event_details( session_get, eventRow['event'] )

        
        if event_response_data:
            #print(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            #logging.info(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            
            update_event_orgunit = event_response_data
            update_event_orgunit["orgUnit"] = eventRow.get("orgUnit")

            #print(f" event_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            #dataValues = event_response_data.get('dataValues',[])
            #events = event_response_data.get('response', {})
            #print(f" update_event_date : {update_event_date}" )
            

            event_update_orgunit_payload = {
                "events": [
                    {
                        "event": eventRow['event'],
                        "program": event_response_data.get('program'),
                        "programStage": event_response_data.get('programStage'),
                        "orgUnit": eventRow.get("orgUnit"),
                        "occurredAt": event_response_data.get("occurredAt")
                    }
                ]
            }

            executor.submit( update_event_orgunit_in_dhis2_242_xlsx, session_get, event_update_orgunit_payload, eventRow['event'], eventRow.get("orgUnit"), index+1 )
        
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"event orgUnit update end . { current_time_end }" )
logging.info(f"event orgUnit update end . { current_time_end }")

