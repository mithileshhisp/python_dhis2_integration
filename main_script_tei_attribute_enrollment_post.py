#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import openpyxl
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
dhis2_username = "*****"
dhis2_password = "*****"

from constants import LOG_FILE_TEI_ATTRIBUTE_ENROLLMENT_POST, LOG_FILE_EVENT_ERROR_LOG

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

logging.basicConfig(filename=LOG_FILE_TEI_ATTRIBUTE_ENROLLMENT_POST, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

trackedEntityType = "MCPQUTHX1Ze"
selectedProgram = "bASezt1TUKD"

#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"tei and enrollment post start . { current_time_start }" )
logging.info(f"tei and enrollment post start . { current_time_start }")

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
    event_get_url = f"{DHIS2_API_GET_URL}/events/{event_uid}.json"

    #print(event_search_url)
    #print(f" event_search_url : {event_search_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session_get.get(event_get_url)
    if response.status_code == 200:
        event_response_data = response.json()
        
        print(f" event_response_data trackedEntityInstance : {event_response_data.get('trackedEntityInstance')}" )
        dataValues = event_response_data.get('dataValues',[])
        #events = event_response_data.get('response', {})
        print(f" dataValues : {dataValues}" )
        return event_response_data 
    else:
        return []

def assign_value_if_not_null(value):
    if value is not None and value != "null":
        return value
    else:
        return ""


def assign_value_if_NaN(value):
    if pd.notnull(value):
        if isinstance(value, int):
            return value
        elif isinstance(value, float):
            return value
        elif value == 'NULL':
            return ""
        else:
            return str(value)
    
    else:
        return ""

def float_to_int(val):     
    if val=='' or pd.isna(val):
        return ''
    else:
        return int(val)  

def push_tei_enrollment_in_dhis2(session_post, enrollment_data, org_uid, enrollment_date, tei_uid, row ):
    #
    try:
        enrollment_endpoint = f"{DHIS2_API_POST_URL}trackedEntityInstances"
        enrollment_data["enrollments"][0]["orgUnit"] = org_uid
        enrollment_data["enrollments"][0]["enrollmentDate"] = enrollment_date
        enrollment_data["enrollments"][0]["incidentDate"] = enrollment_date

        response = session_post.post(enrollment_endpoint, data=json.dumps(enrollment_data), headers={"Content-Type": "application/json"})
        response.raise_for_status()

        if response.status_code == 200:
            logging.info(f"Enrollment created successfully for row : {row}, tei_uid : {tei_uid} . orgUnit Id : {org_uid}")
            print(f"Enrollment created successfully for row : {row}, tei_uid : {tei_uid}, orgUnit Id : {org_uid}")
        else:
            logging.error(f"Failed to create enrollment for row : {row}, tei_uid {tei_uid}, orgUnit Id : {org_uid} . Status code: {response.status_code} . error details: {response.json()}")

    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        #print(f'####################################################### FAILED #######################################################', flush=True)
        #print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
        print(f" Failed to create events. Error: {response.text}")
        logging.error(f" Failed to create events .tei_uid : {tei_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

        with open(LOG_FILE_EVENT_ERROR_LOG, 'a') as fail_record:
            fail_record.write(f'\ncurrent tei_uid: {tei_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f"Failed to create events. Error: {response.text}")
        logging.error(f"Failed to create events . tei_uid : {tei_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


tei_enrollment_post_excel_file_path = 'teiAttributesEnrollmentPost.xlsx'
print( f" file_name . { tei_enrollment_post_excel_file_path }" )
logging.info(f" file_name . { tei_enrollment_post_excel_file_path }")
tei_list = pd.read_excel(tei_enrollment_post_excel_file_path)

with ThreadPoolExecutor(max_workers=10) as executor:
    # Create a session object for persistent connection
    
    headers = list(tei_list.columns)

    print("List of column names:", headers)
    
    '''
    for row in range(0, dataframe1.max_row):
    for col in dataframe1.iter_cols(1, dataframe1.max_column):
        print(col[row].value)
    '''


    # Define variable to load the dataframe
    dataframe = openpyxl.load_workbook(tei_enrollment_post_excel_file_path)

    # Define variable to read sheet
    dataframe1 = dataframe.active

    # Iterate the loop to read the cell values
    for row in range(0, dataframe1.max_row):
        for col in dataframe1.iter_cols(6, dataframe1.max_column):
            print(col[row].value)
            #print(  row, col, col[row].value)
            #print(  row[col].value )


    for index, teiRow in tei_list.iterrows():
        for col in tei_list.columns(5, tei_list.columns):
            print(col[teiRow].value)
            print(f"Row {index + 1}: {col} -- {teiRow[col]}" )
            #print(f"Row {index + 1}: {eventRow}" )
            #print(f"Row {index + 1} " )
            #event_response_data = get_event_details( session_get, teiRow['event_from'] )

            '''
            enrollment_data = {

            
                "trackedEntityType": trackedEntityType,
                "trackedEntityInstance": teiRow['tei'],
                "orgUnit": teiRow['orgunit'],
                "attributes": [
                    {"attribute": "P3Spi0kT92n", "value": str(assign_value_if_NaN(teiRow['ClientID']))},
                    {"attribute": "n2gG7cdigPc", "value": str(assign_value_if_NaN(teiRow['PrEPIDNumber']))},
                    {"attribute": "m5ooA17z7xD", "value": str(assign_value_if_NaN(teiRow['MPI']))}
                ],
                "enrollments": [
                    {
                        "status": "ACTIVE",
                        "program": selectedProgram,
                        "orgUnit": teiRow['orgunit'],
                        "enrollmentDate": teiRow['enrollmentDate'],
                        "incidentDate": teiRow['enrollmentDate']
                    }
                ]

                #response = create_enrollment(enrollment_data, org_unit_id,CreatedDate)
            }
            '''
        #executor.submit( push_tei_enrollment_in_dhis2, session_post, enrollment_data, teiRow['orgunit'], teiRow['enrollmentDate'], teiRow['tei'], index+1 )


        
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"tei and enrollment post end . { current_time_end }" )
logging.info(f"tei and enrollment post end . { current_time_end }")

