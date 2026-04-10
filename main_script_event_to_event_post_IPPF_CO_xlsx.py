#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth

import urllib3 ## for disable warning of Certificate
urllib3.disable_warnings() ## for disable warning of Certificate


from constants import LOG_FILE_EVENT_POST, LOG_FILE_EVENT_ERROR_LOG

# DHIS2 API credentials and URL



DHIS2_API_GET_URL = "******/api/"
DHIS2_AUTH_GET = ("*****", "*****")


DHIS2_API_POST_URL = "******/api/"
DHIS2_AUTH_POST = ("*****", "*****")

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_EVENT_POST, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"event to event post start . { current_time_start }" )
logging.info(f"event to event post start . { current_time_start }")

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
    #, verify=False
    response = session_get.get(event_get_url, verify=False )
    
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



def push_events_in_dhis2(session_post, event_payload, event_uid, row ):
    #
    try:
        #, verify=False
        event_post_url = f"{DHIS2_API_POST_URL}events"
        response = session_post.post(event_post_url, data=json.dumps(event_payload), verify=False, headers={"Content-Type": "application/json"})
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
event_to_event_post_excel_file_path = 'ippf_co_event_to_event_post.xlsx'

print( f"file_name . { event_to_event_post_excel_file_path }" )
logging.info(f"file_name . { event_to_event_post_excel_file_path }")


with ThreadPoolExecutor(max_workers=10) as executor:
    # Create a session object for persistent connection
    event_list = pd.read_excel(event_to_event_post_excel_file_path)
    for index, eventRow in event_list.iterrows():
        #print(f"Row {index + 1}: {eventRow}" )
        #print(f"Row {index + 1} " )
        event_response_data = get_event_details( session_get, eventRow['event_from'] )

        #print( f" length of event data value . { len(event_response_data) }" )
        #print(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
        #logging.info(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
        #logging.info( f" length of event data value . { len(event_response_data) }" )

        
        if event_response_data:
           
            tempEventDataValues = list(event_response_data.get('dataValues', []))

            data_element_id = 'T1poFhLsB2S'
            new_value = 'Annual Reporting'

            found = False

            for dv in tempEventDataValues:
                if dv.get('dataElement') == data_element_id:
                    dv['value'] = new_value   # ✅ update existing value
                    found = True
                    break

            # If not found, then append
            if not found:
                tempEventDataValues.append({
                    "dataElement": data_element_id,
                    "value": new_value
                })


            event_payload = {
                "event": eventRow['event_to'],
                "program": event_response_data.get('program'),
                "orgUnit": event_response_data.get('orgUnit'),
                "eventDate": event_response_data.get('eventDate'),
                "programStage": event_response_data.get('programStage'),
                "status": event_response_data.get('status'),
                "trackedEntityInstance": event_response_data.get('trackedEntityInstance'),
                "storedBy": event_response_data.get('storedBy'),
                "dataValues": tempEventDataValues
            }

            executor.submit( push_events_in_dhis2, session_post, event_payload, eventRow['event_from'], index+1 )
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"event to event post end . { current_time_end }" )
logging.info(f"event to event post end . { current_time_end }")

