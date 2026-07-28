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

from constants import LOG_FILE_ENROLLMENT_DATE_UPDATE, LOG_FILE_EVENT_ERROR_LOG

# DHIS2 API credentials and URL


#DHIS2_API_GET_URL = "https://hhs.drukhmis.gov.bt/bhutan_hhs/api/"
#DHIS2_AUTH_GET = ("*******", "*******")

DHIS2_API_GET_URL = "https://amrin.hispindia.org/equityamr/api/"
DHIS2_AUTH_GET = ("*******", "*******")


DHIS2_API_POST_URL = "https://amr.hispindia.org/amr_asella/api/"
DHIS2_AUTH_POST = ("*******", "*******")

#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_ENROLLMENT_DATE_UPDATE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Enrollment Geometry update start . { current_time_start }" )
logging.info(f"Enrollment Geometry update start . { current_time_start }")

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

def get_enrollment_details(session_get,enrollment_uid):
    
    #https://ln4.hispindia.org/timor_dev/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
   
    #event_search_url = f"{event_push_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={programID}&status=ACTIVE&skipPaging=true&filter={event_search_dataElement_uid}:eq:{BenCallID}"
    enrollment_get_url = f"{DHIS2_API_GET_URL}enrollments/{enrollment_uid}.json"

    #print(event_search_url)
    #print(f" event_search_url : {event_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session_get.get(enrollment_get_url)
    
    if response.status_code == 200:
        enrollment_response_data = response.json()
        #print(response)
        #print(event_response_data)
       
        
        return enrollment_response_data 
    else:
        return []

def update_enrollmentDate_in_dhis2_xlsx(session, update_enrollment_geometry, enrollmentUID, row_no):

    #print( f" update_enrollment_date . { update_enrollment_geometry }" )
    enrollment_update_url = f"{DHIS2_API_GET_URL}enrollments/{enrollmentUID}"
    #print( f"event_update_url . { event_update_url }" )
    # for IPPF CO BPR add verify=False,
    response = session.put(enrollment_update_url, json=update_enrollment_geometry, headers={"Content-Type": "application/json"})
    
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
        print(f"Enrollments updated successfully. Row No: {row_no}.updated Enrollment: {enrollmentUID}. impCount:{impCount}.updateCount:{updateCount}.ignoreCount:{ignoreCount}")
        logging.info(f"Enrollments updated successfully. Row No : {row_no}. updated Enrollment : {enrollmentUID}. impCount : {impCount} .updateCount : {updateCount} .ignoreCount : {ignoreCount}")
        #logging.info(f"Event created successfully . BenVisitID : {BenVisitID} . BeneficiaryRegID : {BeneficiaryRegID}. Event count: {event_count}. Event uid: {event_uid}" )
        #logging.info("MySQL connection closed")

    else:
        print(f"Failed to update events. Error: {response.text}")
        logging.error(f"Failed to update events. Row No : {row_no} .conflictsDetails : {conflictsDetails} .Status code: {response.status_code} .error details: {response.json()} .Error: {response.text}")




#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
enrollment_geometry_update_excel_file_path = 'enrollmentGeometryUpdate.xlsx'

print( f"file_name . { enrollment_geometry_update_excel_file_path }" )
logging.info(f"file_name . { enrollment_geometry_update_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    enrollmenr_list = pd.read_excel(enrollment_geometry_update_excel_file_path)
    print( f"enrollment count . { len(enrollmenr_list) }" )
    logging.info(f"enrollment count . { len(enrollmenr_list) }")
    for index, enrollemntRow in enrollmenr_list.iterrows():
        #print(f"Row {index + 1}: {eventRow}" )
        #print(f"Row {index + 1} " )
        enrollment_response_data = get_enrollment_details( session_get, enrollemntRow['enrollment'] )

        
        if enrollment_response_data:
            #print(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            #logging.info(f" event_get_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            
            update_enrollment_geometry = enrollment_response_data
            update_enrollment_geometry["geometry"] = {
                "type": enrollemntRow['type'],
                "coordinates": [enrollemntRow['latitude'], enrollemntRow['longitude']]
            }

           
            #print(f" event_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
            #dataValues = event_response_data.get('dataValues',[])
            #events = event_response_data.get('response', {})
            #print(f" update_enrollment_date : {update_enrollment_geometry}" )
            
            executor.submit( update_enrollmentDate_in_dhis2_xlsx, session_get, update_enrollment_geometry, enrollemntRow['enrollment'], index+1 )
        
        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Enrollment Geometry update end . { current_time_end }" )
logging.info(f"Enrollment Geometry update end . { current_time_end }")

