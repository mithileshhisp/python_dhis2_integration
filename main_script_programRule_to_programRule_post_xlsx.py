#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
dhis2_username = "*******"
dhis2_password = "******"

from constants import LOG_FILE_PROGRAMRULE_POST, LOG_FILE_PROGRAMRULE_ERROR_LOG

# DHIS2 API credentials and URL


DHIS2_API_GET_URL = "https://mbdrtraining.moh.gov.mm/dhis/api/" 
DHIS2_AUTH_GET = ("*******", "******") ## sumit_hisp #iSp@1234

#DHIS2_API_POST_URL = "https://mbdr.mm.dhis2.net/dhis/api/"
#DHIS2_AUTH_POST = ("*******", "*****")

DHIS2_API_POST_URL =  "https://hmistraining.mm.dhis2.net/train/api/" ### event training
DHIS2_AUTH_POST = ("*******", "*******")

#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_PROGRAMRULE_POST, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"programrule to programrule post start . { current_time_start }" )
logging.info(f"programrule to programrule post start . { current_time_start }")

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

def get_programRule_details(session_get, programrule_uid):
    
    #https://ln4.hispindia.org/timor_dev/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
   
    #event_search_url = f"{event_push_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={programID}&status=ACTIVE&skipPaging=true&filter={event_search_dataElement_uid}:eq:{BenCallID}"
    program_rule_get_url = f"{DHIS2_API_GET_URL}programRules/{programrule_uid}.json"

    print(program_rule_get_url)
    #print( f"program_rule_get_url . { program_rule_get_url }" )
    #print(f" event_search_url : {event_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session_get.get(program_rule_get_url)
    #print( f"response . { response }" )
    if response.status_code == 200:
        #print( f"response . { response }" )
        program_rule_response_data = response.json()
        #print(response)
        
        #print(program_rule_response_data)
        #print( f"program_rule_response_data . { program_rule_response_data }" )
        return program_rule_response_data 
    else:
        return []



def push_programrule_in_dhis2(session_post, programrule_payload, programrule_uid, row ):
    #
    #print(f"programrule_payload post.  {programrule_payload}")
    try:
        programRule_post_url = f"{DHIS2_API_POST_URL}programRules"
        response = session_post.post(programRule_post_url, data=json.dumps(programrule_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        #print(f"response post.  {response.json()}")
        #print('####################################################### SUCCESSFUL ##########################################################', flush=True)
        print(f"ProgramRules created successfully. programrule_uid : {programrule_uid} . row : {row}  imported Programrule : {programrule_uid}")
        logging.info(f"ProgramRules created successfully. programrule_uid : {programrule_uid} . row : {row} imported Programrule : {programrule_uid}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        
        with open(LOG_FILE_PROGRAMRULE_ERROR_LOG, 'a') as fail_record:
            fail_record.write(f'\ncurrent programrule_uid: {programrule_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f" Failed to create ProgramRules. programrule_uid : {programrule_uid}  Error: {response.text}")
        logging.error(f"Failed to create ProgramRules programrule_uid : {programrule_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
programRule_to_programRule_post_excel_file_path = 'programRule_to_programRule_post.xlsx'

print( f"file_name . { programRule_to_programRule_post_excel_file_path }" )
logging.info(f"file_name . { programRule_to_programRule_post_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    programRule_list = pd.read_excel(programRule_to_programRule_post_excel_file_path)
    print( f"programRule count . { len(programRule_list) }" )
    logging.info(f"programRule count . { len(programRule_list) }")
    for index, programRuleRow in programRule_list.iterrows():
        #print(f"Row {index + 1}: {eventRow}" )
        #print(f"Row {index + 1} " )
        program_rule_response_data = get_programRule_details( session_get, programRuleRow['programrule_from'] )

        #print( f" length of event data value . { len(event_response_data) }" )
        #print(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
        #logging.info(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
        #logging.info( f" length of event data value . { len(event_response_data) }" )

        
        if program_rule_response_data:
            #print(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            #logging.info(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            
            #programRule_payload = program_rule_response_data
            programRule_payload = program_rule_response_data.copy()
            programRule_payload["id"] = programRuleRow['programrule_to']
            programRule_payload["program"] = { "id" : programRuleRow['program']}
            #programRule_payload["href"] = f"{DHIS2_API_POST_URL}programRules/{programRuleRow['programrule_to']}"
            #'href': 'https://links.hispindia.org/myr_registry/api/programRules/GOMzMSKlZsq'

            executor.submit( push_programrule_in_dhis2, session_post, programRule_payload, programRuleRow['programrule_from'], index+1 )
        
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"programrule to programrule post end . { current_time_end }" )
logging.info(f"programrule to programrule post end . { current_time_end }")

