#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
dhis2_username = "hispdev"
dhis2_password = "Devhisp@1"

from constants import LOG_FILE_TEI_POST, LOG_FILE_TEI_ERROR_LOG

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

logging.basicConfig(filename=LOG_FILE_TEI_POST, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"tei to tei post start . { current_time_start }" )
logging.info(f"tei to tei post start . { current_time_start }")

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

def get_tei_details(session_get,tei_uid):
    
    #https://ln4.hispindia.org/timor_dev/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
   
    #event_search_url = f"{event_push_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={programID}&status=ACTIVE&skipPaging=true&filter={event_search_dataElement_uid}:eq:{BenCallID}"
    tei_get_url = f"{DHIS2_API_GET_URL}trackedEntityInstances/{tei_uid}.json?fields=*"

    #print(tei_get_url)
    #print(f" event_search_url : {event_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session_get.get(tei_get_url)
    #print(response)
    if response.status_code == 200:
        tei_response_data = response.json()
        #print(response)
        #print(tei_response_data)
       
        #print(f"event_response_data trackedEntityInstance : {tei_response_data.get('trackedEntityInstance')}" )
        enrollments = tei_response_data.get('enrollments',[])
        #tei = tei_response_data.get('response', {})
        #print(f" enrollments : {enrollments}" )
        return tei_response_data 
    else:
        return []

def push_teis_in_dhis2(session_post, tei_payload, tei_uid, row ):
    #
    try:
        tei_post_url = f"{DHIS2_API_POST_URL}trackedEntityInstances"
        response = session_post.post(tei_post_url, data=json.dumps(tei_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        #print('####################################################### SUCCESSFUL ##########################################################', flush=True)
        #print(f'RECORD NO.: {record_count}   current benID: {row["BeneficiaryRegID"]}', flush=True)
        #imported_event_uid = response.json().get("response", {}).get("importSummaries", [])[0].get("reference")
        #event_ids = [item.get("event") for item in response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")]
        #print(f"Events created successfully. Event IDs: {response.json()}")
        #event_count = response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")
        print(f"TrackedEntityInstance created successfully. tei_uid : {tei_uid} . row : {row} ")
        logging.info(f"TrackedEntityInstance created successfully. tei_uid : {tei_uid} . row : {row} ")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        #print(f'####################################################### FAILED #######################################################', flush=True)
        #print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
        #print(f"Failed to create events. Error: {response.text}")
        #logging.error(f"Failed to create events .event_uid : {event_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

        with open(LOG_FILE_TEI_ERROR_LOG, 'a') as fail_record:
            fail_record.write(f'\ncurrent tei_uid: {tei_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f"Failed to create TrackedEntityInstance. Error: {response.text}")
        logging.error(f"Failed to create TrackedEntityInstance . tei_uid : {tei_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
tei_to_tei_post_excel_file_path = 'tei_to_tei_post.xlsx'

print( f"file_name . { tei_to_tei_post_excel_file_path }" )
logging.info(f"file_name . { tei_to_tei_post_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    tei_list = pd.read_excel(tei_to_tei_post_excel_file_path)
    print( f"tei count . { len(tei_list) }" )
    logging.info(f"tei count . { len(tei_list) }")
    for index, teiRow in tei_list.iterrows():
        #print(f"Row {index + 1}: {eventRow}" )
        #print(f"Row {index + 1} " )
        tei_response_data = get_tei_details( session_get, teiRow['tei_from'] )

        if tei_response_data:
            #print(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            #logging.info(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            tei_payload = tei_response_data

            executor.submit( push_teis_in_dhis2, session_post, tei_payload, teiRow['tei_from'], index+2 )
        
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"tei to tei post end . { current_time_end }" )
logging.info(f"tei to tei post end . { current_time_end }")

