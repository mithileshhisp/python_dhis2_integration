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

from constants import LOG_FILE_DELETE_ENROLLMENT_XLSX, LOG_FILE_DELETE_ENROLLMENT_ERROR_LOG_XLSX

# DHIS2 API credentials and URL

DHIS2_API_GET_URL = "https://bpr.ippf.org/api/"
DHIS2_AUTH_GET = ("*******", "*******")

dhis2_username = "******"
dhis2_password = "******"

#DHIS2_API_POST_URL = "https://hhs.drukhmis.gov.bt/bhutan_hhs/api/"
#DHIS2_AUTH_POST = ("*******", "*******")

#DHIS2_API_POST_URL = "https://links.hispindia.org/pmnpis_dev/api/"
#DHIS2_API_POST_URL = "https://pmnpis.org.ph/app/api/"
#DHIS2_AUTH_POST = ("*******", "*******")


#DHIS2_API_POST_URL = "https://mbdr.moh.gov.mm/dhis/api/tracker/" # for 2.42
#DHIS2_AUTH_POST = ("*******", "*******")

DHIS2_API_POST_URL = "https://lllmis.org/dhis/api/" ## production
DHIS2_AUTH_POST = ("*******", "*******")



#DHIS2_API_POST_URL = "https://pmnpis.org.ph/app/api/"
#DHIS2_AUTH_POST = ("data_integration", "*******")
#DHIS2_AUTH_POST = ("*******", "*******")

#DHIS2_API_POST_URL = "https://bpr.ippf.org/api/"
#DHIS2_AUTH_POST = ("*******", "*******")

#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_DELETE_ENROLLMENT_XLSX, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Enrollment Delete start . { current_time_start }" )
logging.info(f"Enrollment Delete start . { current_time_start }")


def delete_enrollment_in_dhis2(session_post, enrollment_uid, row ):
    #
    try:
        #, verify=False
        delete_enrollment_url = f"{DHIS2_API_POST_URL}enrollments/{enrollment_uid}"
        response = session_post.delete(delete_enrollment_url, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        description   = response.json().get("response", {}).get("description")
       
        print(f"Enrollment Deleted successfully. uid : {enrollment_uid}. row : {row}. {description}")
        #print(f"Row : {row}. {description}")
        logging.info(f"Enrollment Deleted successfully. uid  : {enrollment_uid}. row : {row}. {description} ")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
       
        with open(LOG_FILE_DELETE_ENROLLMENT_ERROR_LOG_XLSX, 'a') as fail_record:
            fail_record.write(f'\ncurrent event_uid: {enrollment_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f" Failed to Delete Enrollment Error: {response.text}")
        logging.error(f" Failed to Delete Enrollment .UID : {enrollment_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
#enrollments_post_api_excel_file_path = 'enrollments_post_api.xlsx'
#delete_event_excel_file_path = 'delete_events_pmnp.xlsx'
delete_enrollment_excel_file_path = 'delete_enrollments.xlsx'

print( f"file_name . { delete_enrollment_excel_file_path }" )
logging.info(f"file_name . { delete_enrollment_excel_file_path }")


with ThreadPoolExecutor(max_workers=10) as executor:
    # Create a session object for persistent connection
    enrollment_list = pd.read_excel(delete_enrollment_excel_file_path)
    print( f"length of enrollment_list. { len(enrollment_list) }" )
    logging.info( f"length of enrollment_list . { len(enrollment_list) }" )
    for index, enrollment_Row in enrollment_list.iterrows():
        
        enrollment_uid =  enrollment_Row['enrollment']

        executor.submit( delete_enrollment_in_dhis2, session_post, enrollment_uid,  index+1 )
        
           
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Enrollment Delete end . { current_time_end }" )
logging.info(f"Enrollment Delete end . { current_time_end }")

