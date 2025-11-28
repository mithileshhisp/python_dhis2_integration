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

from constants import LOG_FILE_DELETE_TEI_XLSX, LOG_FILE_DELETE_TEI_ERROR_LOG_XLSX

# DHIS2 API credentials and URL


DHIS2_API_GET_URL = "****/api/"
DHIS2_AUTH_GET = ("*****", "*****")


DHIS2_API_POST_URL = "****/api/"
DHIS2_AUTH_POST = ("****", "*****")

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_DELETE_TEI_XLSX, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" TrackedEntityInstance Delete start . { current_time_start }" )
logging.info(f" TrackedEntityInstance Delete start . { current_time_start }")


def delete_trackedEntityInstance_in_dhis2(session_post, tei_uid, row ):
    #
    try:
        #, verify=False
        delete_trackedEntityInstance_url = f"{DHIS2_API_POST_URL}trackedEntityInstances/{tei_uid}"
        response = session_post.delete(delete_trackedEntityInstance_url, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        description   = response.json().get("response", {}).get("description")
        #print('####################################################### SUCCESSFUL ##########################################################', flush=True)
        #print(f'RECORD NO.: {record_count}   current benID: {row["BeneficiaryRegID"]}', flush=True)
        #imported_enrollment_uid = response.json().get("response", {}).get("importSummaries", [])[0].get("reference")
        #event_ids = [item.get("event") for item in response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")]
        #print(f"Events created successfully. Event IDs: {response.json()}")
        #enrollment_count = response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")
        print(f" TEI Delete successfully. uid : {tei_uid}. row : {row}. {description}")
        logging.info(f" TEI Delete successfully. uid  : {tei_uid}. row : {row}. {description} ")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        #print(f'####################################################### FAILED #######################################################', flush=True)
        #print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
        #print(f"Failed to create events. Error: {response.text}")
        #logging.error(f"Failed to create events .event_uid : {event_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

        with open(LOG_FILE_DELETE_TEI_ERROR_LOG_XLSX, 'a') as fail_record:
            fail_record.write(f'\ncurrent tei_uid: {tei_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f" Failed to Delete TEI Error: {response.text}")
        logging.error(f" Failed to Delete TEI .UID : {tei_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
#enrollments_post_api_excel_file_path = 'enrollments_post_api.xlsx'
delete_trackedEntityInstances_excel_file_path = 'delete_trackedEntityInstances.xlsx'


print( f"file_name . { delete_trackedEntityInstances_excel_file_path }" )
logging.info(f"file_name . { delete_trackedEntityInstances_excel_file_path }")


with ThreadPoolExecutor(max_workers=10) as executor:
    # Create a session object for persistent connection
    trackedEntityInstance_list = pd.read_excel(delete_trackedEntityInstances_excel_file_path)
    print( f"length of event_list. { len(trackedEntityInstance_list) }" )
    logging.info( f"length of event_list . { len(trackedEntityInstance_list) }" )
    for index, trackedEntityInstanceRow in trackedEntityInstance_list.iterrows():
        
        teiUid =  trackedEntityInstanceRow['trackedEntityInstance']

        executor.submit( delete_trackedEntityInstance_in_dhis2, session_post, teiUid,  index+1 )
        
           
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" TrackedEntityInstance Delete end . { current_time_end }" )
logging.info(f" TrackedEntityInstance Delete end . { current_time_end }")

