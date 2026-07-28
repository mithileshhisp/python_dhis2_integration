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
dhis2_password = "*******"

from constants import LOG_FILE_DELETE_PROGRAM_RULE_XLSX, LOG_FILE_DELETE_PROGRAM_RULE_ERROR_LOG_XLSX

# DHIS2 API credentials and URL

DHIS2_API_GET_URL = "https://bpr.ippf.org/api/"
DHIS2_AUTH_GET = ("*******", "*******")

dhis2_username = "*******"
dhis2_password = "******"

#DHIS2_API_POST_URL = "https://hhs.drukhmis.gov.bt/bhutan_hhs/api/"
#DHIS2_AUTH_POST = ("*******", "*******")

#DHIS2_API_POST_URL = "https://links.hispindia.org/pmnpis_dev/api/"
#DHIS2_API_POST_URL = "https://pmnpis.org.ph/app/api/"
#DHIS2_AUTH_POST = ("*******", "*******")


#DHIS2_API_POST_URL = "https://mbdr.moh.gov.mm/dhis/api/tracker/" # for 2.42
#DHIS2_AUTH_POST = ("*******", "*******")

DHIS2_API_POST_URL =  "https://hmistraining.mm.dhis2.net/train/api/" ### event training
DHIS2_AUTH_POST = ("*******", "******")

#DHIS2_API_POST_URL = "https://pmnpis.org.ph/app/api/"
#DHIS2_AUTH_POST = ("********", "*******")
#DHIS2_AUTH_POST = ("*******", "*******")

#DHIS2_API_POST_URL = "https://bpr.ippf.org/api/"
#DHIS2_AUTH_POST = ("*******", "*******")

#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_DELETE_PROGRAM_RULE_XLSX, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" Program Rule Delete start . { current_time_start }" )
logging.info(f" Program Rule Delete start . { current_time_start }")


def delete_program_rule_in_dhis2(session_post, program_rule_uid, row ):
    #
    try:
        #, verify=False
        delete_trackedEntityInstance_url = f"{DHIS2_API_POST_URL}programRules/{program_rule_uid}"
        response = session_post.delete(delete_trackedEntityInstance_url, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        description   = response.json()
       
        print(f" Program Rule Deleted successfully. uid : {program_rule_uid}. row : {row}. {description}")
        logging.info(f" Program Rule Deleted successfully. uid  : {program_rule_uid}. row : {row}. {description} ")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        
        with open(LOG_FILE_DELETE_PROGRAM_RULE_ERROR_LOG_XLSX, 'a') as fail_record:
            fail_record.write(f'\n current event_uid: {program_rule_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f" Failed to Delete Program Rule Error: {response.text}")
        logging.error(f" Failed to Delete Program Rule .UID : {program_rule_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")



delete_program_rule_excel_file_path = 'delete_program_rule.xlsx'

print( f"file_name . { delete_program_rule_excel_file_path }" )
logging.info(f"file_name . { delete_program_rule_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    program_rule_list = pd.read_excel(delete_program_rule_excel_file_path)
    print( f"length of program_rule_list. { len(program_rule_list) }" )
    logging.info( f"length of program_rule_list . { len(program_rule_list) }" )
    for index, eventRow in program_rule_list.iterrows():
        
        program_rule_uid =  eventRow['program_rule_uid']

        executor.submit( delete_program_rule_in_dhis2, session_post, program_rule_uid,  index+1 )
        
           
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" Program Rule Delete end . { current_time_end }" )
logging.info(f" Program Rule Delete end . { current_time_end }")

