#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth


from constants import LOG_FILE_DELETE_EVENT_XLSX, LOG_FILE_DELETE_EVENT_ERROR_LOG_XLSX

# DHIS2 API credentials and URL

DHIS2_API_GET_URL = "******/api/"
DHIS2_AUTH_GET = ("******", "*****")

dhis2_username = "******"
dhis2_password = "******"

#DHIS2_API_POST_URL = "******/api/"
#DHIS2_AUTH_POST = ("*******", "*******")

#DHIS2_API_POST_URL = "******/api/"
#DHIS2_API_POST_URL = "******/api/"
#DHIS2_AUTH_POST = ("*******", "*******")

#https://mbdr.moh.gov.mm/dhis/api/tracker/events/bo9EnvkjuZ8.json
DHIS2_API_POST_URL = "*****/dhis/api/42/" # for 2.42
DHIS2_AUTH_POST = ("*****", "******")


# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_DELETE_EVENT_XLSX, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" Event Delete start . { current_time_start }" )
logging.info(f" Event Delete start . { current_time_start }")


def delete_event_in_dhis2(session_post, event_uid, row ):
    #
    try:
        #, verify=False
        delete_trackedEntityInstance_url = f"{DHIS2_API_POST_URL}events/{event_uid}"
        response = session_post.delete(delete_trackedEntityInstance_url, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        description   = response.json().get("response", {}).get("description")
        #print('####################################################### SUCCESSFUL ##########################################################', flush=True)
        #print(f'RECORD NO.: {record_count}   current benID: {row["BeneficiaryRegID"]}', flush=True)
        #imported_enrollment_uid = response.json().get("response", {}).get("importSummaries", [])[0].get("reference")
        #event_ids = [item.get("event") for item in response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")]
        #print(f"Events created successfully. Event IDs: {response.json()}")
        #enrollment_count = response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")
        print(f" Event Deleted successfully. uid : {event_uid}. row : {row}. {description}")
        logging.info(f" Event Deleted successfully. uid  : {event_uid}. row : {row}. {description} ")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        #print(f'####################################################### FAILED #######################################################', flush=True)
        #print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
        #print(f"Failed to create events. Error: {response.text}")
        #logging.error(f"Failed to create events .event_uid : {event_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

        with open(LOG_FILE_DELETE_EVENT_ERROR_LOG_XLSX, 'a') as fail_record:
            fail_record.write(f'\ncurrent event_uid: {event_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f" Failed to Delete TEI Error: {response.text}")
        logging.error(f" Failed to Delete TEI .UID : {event_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")



def delete_event_in_dhis2_242(event_delete_payload, batch_size):
    #
    try:
        
        url = f"{DHIS2_API_POST_URL}tracker?async=false&importStrategy=DELETE"
        #https://mbdr.moh.gov.mm/dhis/api/42/tracker?async=false&importStrategy=DELETE
        response = session_post.post(
            url,
            json=event_delete_payload,
            headers={"Content-Type": "application/json"}
        )

        print(f"Batch {i//batch_size + 1} Status:", response.status_code)
        #print(response.json())

        print(f"Batch {i//batch_size + 1} Status:, {response.status_code} ")
        logging.info(f"Batch {i//batch_size + 1} Status:, {response.status_code}, response  {response.json()}" )
        
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        #print(f'####################################################### FAILED #######################################################', flush=True)
        #print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
        #print(f"Failed to create events. Error: {response.text}")
        #logging.error(f"Failed to create events .event_uid : {event_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

        print(f" Failed to Delete TEI Error: {response.text}")
        logging.error(f" Failed to Delete Event Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")



#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
#enrollments_post_api_excel_file_path = 'enrollments_post_api.xlsx'
#delete_event_excel_file_path = 'delete_events_pmnp.xlsx'
#delete_event_excel_file_path = 'delete_events.xlsx'


# 🔹 Read Excel
delete_event_excel_file_path = "delete_events.xlsx"
df = pd.read_excel(delete_event_excel_file_path)

print( f"file_name . { delete_event_excel_file_path }" )
logging.info(f"file_name . { delete_event_excel_file_path }")

event_list = df["event_uid"].dropna().tolist()

print(f"Total events to delete: {len(event_list)}")

# 🔹 Batch size (recommended 50–100 per call)
batch_size = 50

for i in range(0, len(event_list), batch_size):
    batch = event_list[i:i+batch_size]

    event_delete_payload = {
        "events": [
            {
                "event": event_uid
            }
            for event_uid in batch
        ]
    }


    delete_event_in_dhis2_242( event_delete_payload, batch_size )

           
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Event Delete end . { current_time_end }" )
logging.info(f"Event Delete end . { current_time_end }")

