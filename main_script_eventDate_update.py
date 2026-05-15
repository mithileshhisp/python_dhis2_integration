#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth


from constants import LOG_FILE_EVENT_DATE_UPDATE, LOG_FILE_EVENT_ERROR_LOG

# DHIS2 API credentials and URL



DHIS2_API_GET_URL = "*******/api/"
DHIS2_AUTH_GET = ("******", "******")


DHIS2_API_POST_URL = "*******/api/"
DHIS2_AUTH_POST = ("******", "******")

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_EVENT_DATE_UPDATE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"event event_date update start . { current_time_start }" )
logging.info(f"event event_date update start . { current_time_start }")

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
    event_get_url = f"{DHIS2_API_GET_URL}events/{event_uid}.json"

    #print(event_search_url)
    #print(f" event_search_url : {event_get_url}" )
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

def update_eventDate_in_dhis2_xlsx(session, update_event_date, eventUID, event_date, row_no):

    #print( f" updateEventDataValue . { updateEventDataValue }" )
    event_update_url = f"{DHIS2_API_GET_URL}events/{eventUID}"
    #print( f"event_update_url . { event_update_url }" )
    # for IPPF CO BPR add verify=False,
    response = session.put(event_update_url, json=update_event_date, headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        conflictsDetails   = response.json().get("response", {}).get("conflicts")
        #description   = response.json().get("response", {}).get("description")
        impCount = response.json().get("response", {}).get("importCount").get("imported")
        updateCount = response.json().get("response", {}).get("importCount").get("updated")
        ignoreCount = response.json().get("response", {}).get("importCount").get("ignored")
        #event_uid = response.json().get("response", {}).get("importSummaries", [])[0].get("reference")
        #event_ids = [item.get("event") for item in response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")]
        #print(f"Events created successfully. Event IDs: {response.json()}")
        #event_count = response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")
        print(f"Events updated successfully. Row No: {row_no}.updated event: {eventUID}.with event_date {event_date} impCount:{impCount}.updateCount:{updateCount}.ignoreCount:{ignoreCount}")
        logging.info(f"Events updated successfully. Row No : {row_no}. updated event : {eventUID}. with event_date {event_date} impCount : {impCount} .updateCount : {updateCount} .ignoreCount : {ignoreCount}")
        #logging.info(f"Event created successfully . BenVisitID : {BenVisitID} . BeneficiaryRegID : {BeneficiaryRegID}. Event count: {event_count}. Event uid: {event_uid}" )
        #logging.info("MySQL connection closed")

    else:
        print(f"Failed to update events. Error: {response.text}")
        logging.error(f"Failed to update events. Row No : {row_no} .conflictsDetails : {conflictsDetails} .Status code: {response.status_code} .error details: {response.json()} .Error: {response.text}")


def push_events_in_dhis2(session_post, event_payload, event_uid, row ):
    #
    try:
        event_post_url = f"{DHIS2_API_POST_URL}events"
        response = session_post.post(event_post_url, data=json.dumps(event_payload), headers={"Content-Type": "application/json"})
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


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
event_date_update_excel_file_path = 'eventDateUpdate.xlsx'

print( f"file_name . { event_date_update_excel_file_path }" )
logging.info(f"file_name . { event_date_update_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    event_list = pd.read_excel(event_date_update_excel_file_path)
    print( f"event count . { len(event_list) }" )
    logging.info(f"event count . { len(event_list) }")
    for index, eventRow in event_list.iterrows():
        #print(f"Row {index + 1}: {eventRow}" )
        #print(f"Row {index + 1} " )
        event_response_data = get_event_details( session_get, eventRow['event'] )

        
        if event_response_data:
            #print(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            #logging.info(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            
            update_event_date = event_response_data
            update_event_date["eventDate"] = eventRow.get("eventDate")

            #print(f" event_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            #dataValues = event_response_data.get('dataValues',[])
            #events = event_response_data.get('response', {})
            #print(f" update_event_date : {update_event_date}" )
            
            executor.submit( update_eventDate_in_dhis2_xlsx, session_get, update_event_date, eventRow['event'], eventRow.get("eventDate"), index+1 )
        
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"event eventDate update end . { current_time_end }" )
logging.info(f"event eventDate update end . { current_time_end }")

