#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth

dhis2_username = "admin"
dhis2_password = "district"

from constants import LOG_FILE_EVENT_POST, LOG_FILE_EVENT_ERROR_LOG

# DHIS2 API credentials and URL


# DHIS2 API credentials and URL
DHIS2_API_URL = "/api/"
DHIS2_AUTH = ("*****", "*****")




# Create a session object for persistent connection
session = requests.Session()
session.auth = DHIS2_AUTH

logging.basicConfig(filename=LOG_FILE_EVENT_POST, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"event to event post start . { current_time_start }" )
logging.info(f"event to event post start . { current_time_start }")


def get_sqlview_data(session):
    
    # event_list_for_migration = sw9NLEwlWXp
   
    sql_view_url = f"{DHIS2_API_URL}sqlViews/sw9NLEwlWXp/data.json?paging=false"

    print(f"sql_view_url : {sql_view_url}")

    #response_sql_view = requests.get(sql_view_url,auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    
    response_sql_view = session.get(sql_view_url)
    
    print(f"response_sql_view : {response_sql_view.text}")

    if response_sql_view.status_code == 200:
        #print(f"response_sql_view : {response_sql_view.status_code}")
        response_sql_view_data = response_sql_view.json()
        #print(f"response_sql_view_data : {response_sql_view_data}")
        tempListGrid   = response_sql_view.json().get('listGrid', {})
        #print(f"tempListGrid : {tempListGrid}")
        #print(f"title : {tempListGrid.get('title')}")
        tempRows = tempListGrid.get('rows',[])

        if tempRows:
            for rows in tempRows:
                event = rows[0]
                orgUnit = rows[1]
                print(f"event : {event}, orgUnit : {orgUnit}")
                
        else:
            error_message = f"No data received for sqlview"
            print(error_message)

        #print(tempRows)

    else:
        print(f"Failed to retrieve sqlview data. Status code: {response_sql_view.status_code}")

    return tempRows



def get_event_details(session,event_uid):
    
    #https://ln4.hispindia.org/timor_dev/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
   
    #event_search_url = f"{event_push_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={programID}&status=ACTIVE&skipPaging=true&filter={event_search_dataElement_uid}:eq:{BenCallID}"
    event_get_url = f"{DHIS2_API_URL}events/{event_uid}.json"

    #print(event_search_url)
    #print(f" event_search_url : {event_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session.get(event_get_url)
    
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



def push_events_in_dhis2(session, event_payload, event_uid, row ):
    #
    try:
        event_post_url = f"{DHIS2_API_URL}events"
        response = session.post(event_post_url, data=json.dumps(event_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        #print('####################################################### SUCCESSFUL ##########################################################', flush=True)
        #print(f'RECORD NO.: {record_count}   current benID: {row["BeneficiaryRegID"]}', flush=True)
        imported_event_uid = response.json().get("response", {}).get("importSummaries", [])[0].get("reference")
        #event_ids = [item.get("event") for item in response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")]
        #print(f"Events created successfully. Event IDs: {response.json()}")
        event_count = response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")
        print(f"Events created successfully. event_uid : {event_uid} . row : {row} Event count: {event_count}. imported event : {imported_event_uid}")
        logging.info(f"Events created successfully. event_uid : {event_uid} . row : {row} .Event count: {event_count}. imported event : {imported_event_uid}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        #print(f'####################################################### FAILED #######################################################', flush=True)
        #print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
        #print(f"Failed to create events. Error: {response.text}")
        #logging.error(f"Failed to create events .event_uid : {event_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

        with open(LOG_FILE_EVENT_ERROR_LOG, 'a') as fail_record:
            fail_record.write(f'\ncurrent event_uid: {event_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f" Failed to create events. Error: {response.text}")
        logging.error(f"Failed to create events . event_uid : {event_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


with ThreadPoolExecutor(max_workers=10) as executor:
    # Create a session object for persistent connection
    
    sql_views_data = get_sqlview_data(session)
    print( f"length of events. { len(sql_views_data) }" )
    logging.info( f"length of events . { len(sql_views_data) }" )
    #for index, eventDataValueRow in updateEventDataValues.iterrows():
    
    for index, eventUid in enumerate(sql_views_data):
       
        event_response_data = get_event_details( session, eventUid )

        if event_response_data:
            tempEventDataValues = list()
            tempEventDataValues = event_response_data.get('dataValues',[])
            eventDataValue = {
                "dataElement": 'T1poFhLsB2S',
                "value": 'Annual Reporting'
            
            }
            tempEventDataValues.append(eventDataValue)
        
            event_payload = {
                    #"event": event_response_data.get('event'),
                    "program": event_response_data.get('program'),
                    "orgUnit": event_response_data.get('orgUnit'),
                    "eventDate": event_response_data.get('eventDate'),
                    "programStage": event_response_data.get('programStage'),
                    "status": event_response_data.get('status'),
                    "trackedEntityInstance": event_response_data.get('trackedEntityInstance'),
                    "storedBy": event_response_data.get('storedBy'),
                    #"dataValues": event_response_data.get('dataValues',[])
                    "dataValues": tempEventDataValues
                }
            print( f"event_payload . { event_payload }" )
            logging.info(f"event_payload . { event_payload }")
            #executor.submit( push_events_in_dhis2, session, event_payload, eventUid, index+1 )
        

current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"event to event post end . { current_time_end }" )
logging.info(f"event to event post end . { current_time_end }")

