#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth


from constants import LOG_FILE_EVENT_POST_XLSX, LOG_FILE_EVENT_ERROR_LOG_XLSX

# DHIS2 API credentials and URL

DHIS2_API_GET_URL = "https://bpr.ippf.org/api/"
DHIS2_AUTH_GET = ("****", "*****")



DHIS2_API_POST_URL = "https://links.hispindia.org/ippf_uin/api/"
#DHIS2_AUTH_POST = ("****", "*****")

#DHIS2_API_POST_URL = "https://pmnpis.org.ph/app/api/"
#DHIS2_AUTH_POST = ("****", "*****")
DHIS2_AUTH_POST = ("****", "*****")

#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_EVENT_POST_XLSX, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"event to data value post start . { current_time_start }" )
logging.info(f"event to data value  post start . { current_time_start }")

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



def push_events_in_dhis2(session_post, event_payload, event_uid, row ):
    #
    try:
        #, verify=False
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

        with open(LOG_FILE_EVENT_ERROR_LOG_XLSX, 'a') as fail_record:
            fail_record.write(f'\ncurrent event_uid: {event_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f" Failed to create events. Error: {response.text}")
        logging.error(f"Failed to create events . event_uid : {event_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'

#event_to_post_with_out_datavalue_excel_file_path = 'pmnp_event_post_without_data_value.xlsx'
event_to_post_with_out_datavalue_excel_file_path = 'event_post_without_data_value.xlsx'

print( f"file_name . { event_to_post_with_out_datavalue_excel_file_path }" )
logging.info(f"file_name . { event_to_post_with_out_datavalue_excel_file_path }")


with ThreadPoolExecutor(max_workers=10) as executor:
    # Create a session object for persistent connection
    event_list = pd.read_excel(event_to_post_with_out_datavalue_excel_file_path)
    print( f"length of event_list. { len(event_list) }" )
    logging.info( f"length of event_list . { len(event_list) }" )
    for index, eventRow in event_list.iterrows():
        
        tempEventDataValues = []

        event_payload = {
                "event": eventRow['event'],
                "program": eventRow['program'],
                "orgUnit": eventRow['orgUnit'],
                "eventDate": eventRow['eventDate'],
                "programStage": eventRow['programStage'],
                "status": eventRow['status'],
                "trackedEntityInstance": eventRow['trackedEntityInstance'],
                #"storedBy": event_response_data.get('storedBy'),
                #"dataValues": event_response_data.get('dataValues',[]),
                "dataValues": tempEventDataValues
                #"dataValues": [{ "dataElement": eventRow['dataElement'], "value": eventRow['value'] }]  
            }
       
        executor.submit( push_events_in_dhis2, session_post, event_payload, eventRow['event'], index+1 )
        
           
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"event data Value post end . { current_time_end }" )
logging.info(f"event data value post end . { current_time_end }")

