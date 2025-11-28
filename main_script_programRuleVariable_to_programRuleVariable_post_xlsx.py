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

from constants import LOG_FILE_PROGRAMRULE_VARIABLE_POST, LOG_FILE_PROGRAMRULE_VARIABLE_ERROR_LOG

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

logging.basicConfig(filename=LOG_FILE_PROGRAMRULE_VARIABLE_POST, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"programrule variable to programrule variable post start . { current_time_start }" )
logging.info(f"programrule variable to programrule variable post start . { current_time_start }")

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

def get_programRuleVariables_details(session_get, programRuleVariable_uid):
    
    #https://ln4.hispindia.org/timor_dev/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
   
    #event_search_url = f"{event_push_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={programID}&status=ACTIVE&skipPaging=true&filter={event_search_dataElement_uid}:eq:{BenCallID}"
    program_rule_variable_get_url = f"{DHIS2_API_GET_URL}programRuleVariables/{programRuleVariable_uid}.json"

    #print(program_rule_get_url)
    #print( f"program_rule_get_url . { program_rule_get_url }" )
    #print(f" event_search_url : {event_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session_get.get(program_rule_variable_get_url)
    #print( f"response . { response }" )
    if response.status_code == 200:
        #print( f"response . { response }" )
        program_rule_variable_response_data = response.json()
        #print(response)
        
        #print(program_rule_response_data)
        #print( f"program_rule_response_data . { program_rule_response_data }" )
        return program_rule_variable_response_data 
    else:
        return []



def push_programrule_variable_in_dhis2(session_post, programRuleVariable_payload, programRuleVariable_uid, row ):
    #
    #print(f"programrule_payload post.  {programrule_payload}")
    try:
        programRuleVariable_post_url = f"{DHIS2_API_POST_URL}programRuleVariables"
        response = session_post.post(programRuleVariable_post_url, data=json.dumps(programRuleVariable_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        #print(f"response post.  {response}")
        #print('####################################################### SUCCESSFUL ##########################################################', flush=True)
        #print(f'RECORD NO.: {record_count}   current benID: {row["BeneficiaryRegID"]}', flush=True)
        imported_programrule_variable_uid = response.json().get("response", {}).get("importSummaries", [])[0].get("reference")
        #event_ids = [item.get("event") for item in response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")]
        #print(f"Events created successfully. Event IDs: {response.json()}")
        #event_count = response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")
        print(f"programRuleVariables created successfully. programRuleVariable_uid : {programRuleVariable_uid} . row : {row}  imported Programrule : {programRuleVariable_uid}")
        logging.info(f"programRuleVariables created successfully. programRuleVariable_uid : {programRuleVariable_uid} . row : {row} imported Programrule : {programRuleVariable_uid}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        #print(f'####################################################### FAILED #######################################################', flush=True)
        #print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
        #print(f"Failed to create events. Error: {response.text}")
        #logging.error(f"Failed to create events .event_uid : {event_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

        with open(LOG_FILE_PROGRAMRULE_VARIABLE_ERROR_LOG, 'a') as fail_record:
            fail_record.write(f'\ncurrent programRuleVariable_uid: {programRuleVariable_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f" Failed to create programRuleVariable_uid. Error: {response.text}")
        logging.error(f"Failed to create programRuleVariable_uid . programRuleVariable_uid : {programRuleVariable_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
programRuleVariable_to_programRuleVariable_post_excel_file_path = 'programRuleVariable_to_programRuleVariable_post.xlsx'

print( f"file_name . { programRuleVariable_to_programRuleVariable_post_excel_file_path }" )
logging.info(f"file_name . { programRuleVariable_to_programRuleVariable_post_excel_file_path }")


with ThreadPoolExecutor(max_workers=10) as executor:
    # Create a session object for persistent connection
    programRule_variable_list = pd.read_excel(programRuleVariable_to_programRuleVariable_post_excel_file_path)
    print( f"programRule Variable count . { len(programRule_variable_list) }" )
    logging.info(f"programRule Variable count . { len(programRule_variable_list) }")
    for index, programRuleVariableRow in programRule_variable_list.iterrows():
        #print(f"Row {index + 1}: {eventRow}" )
        #print(f"Row {index + 1} " )
        program_rule_variable_response_data = get_programRuleVariables_details( session_get, programRuleVariableRow['programruleVariable_from'] )

        #print( f" length of event data value . { len(event_response_data) }" )
        #print(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
        #logging.info(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
        #logging.info( f" length of event data value . { len(event_response_data) }" )

        
        if program_rule_variable_response_data:
            #print(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            #logging.info(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            
            #programRule_payload = program_rule_response_data
            programRule_variable_payload = program_rule_variable_response_data.copy()
            programRule_variable_payload["id"] = programRuleVariableRow['programruleVariable_to']
            programRule_variable_payload["program"] = { "id" : programRuleVariableRow['program']}
            #programRule_payload["href"] = f"{DHIS2_API_POST_URL}programRules/{programRuleRow['programrule_to']}"
            #'href': 'https://links.hispindia.org/myr_registry/api/programRules/GOMzMSKlZsq'

            executor.submit( push_programrule_variable_in_dhis2, session_post, programRule_variable_payload, programRuleVariableRow['programruleVariable_from'], index+1 )
        
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"programrule variable to programrule variable post end . { current_time_end }" )
logging.info(f"programrule variable to programrule variable post end . { current_time_end }")

