#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
from dhis2_api_interaction import get_org_unit_data, get_tei_data, construct_xlsx_dataValueSet_payload, push_dataValueSet_in_dhis2_xlsx
import database_connection
import logging, datetime
import pandas as pd
from database_connection import connect_to_mysql
import requests
import ssl
import certifi

import urllib3 ## for disable warning of Certificate
urllib3.disable_warnings() ## for disable warning of Certificate

from constants import LOG_FILE_EVENT_DATA_VALUE_UPDATE

logging.basicConfig(filename=LOG_FILE_EVENT_DATA_VALUE_UPDATE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# logging.basicConfig(filename='bayer_event.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#mysql_connection = connect_to_mysql()
#mysql_conn = database_connection.establish_mysql_connection(mysql_host, mysql_port, mysql_user, mysql_password, mysql_database)

# logging.info("MySQL connection closed")

#print("Connected to MySQL database")
#logging.info("Connected to MySQL database")
#cursor = mysql_connection.cursor()

#results = database_connection.fetch_mysql_data(cursor)

#mysql_connection.close()

#dhis2_api_url = "https://hhs.drukhmis.gov.bt/bhutan_hhs/api/"
#un='****'
#pw='*****'

#dhis2_api_url = "https://ln3.hispindia.org/pmnp_is/api/"
#un='****'
#pw='*****'

#dhis2_api_url = "https://dev.pmnpis.org.ph/pmnp_is/api/"
#un='****'
#pw='*****'

#dhis2_api_url = "https://hhs.drukhmis.gov.bt/bhutan_hhs/api/"
#dhis2_api_url = "https://pmnpis.org.ph/app/api/"
#dhis2_api_url =  "http://dss.nipi-cure.org:8665/odk_nipi/api/"

dhis2_api_url = "https://links.hispindia.org/ippf_uin/api/"

#un='****'
#pw='*****'


with requests.Session() as session:
    session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" update evenDataValue start . { current_time_start }" )
logging.info(f" update eventDataValue start . { current_time_start }")

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


def clean_dhis2_value(val):
    #import pandas as pd
    if pd.isna(val) or val is None:
        return ""
    return str(val)

def read_excel_to_dict(file_path):

    dataValueSet = pd.read_excel(file_path)
    #dataValues = []
    dataValues = list()
    #option_dict = {}

    for _, row in dataValueSet.iterrows():
        dataValue = {
            "dataElement": row['dataElementUID'],
            "categoryOptionCombo": row['categoryoptioncomboUID'],
            "value": str(row['dataValue']),
            "period": str(row['isoPeriod']),
        }
        dataValues.append(dataValue)


    return dataValues

#dataValueSet_excel_path = 'dataValueSet_import_ippf_co.xlsx' 
#dataValues = read_excel_to_dict(dataValueSet_excel_path)


#eventDataValue_update_excel_file_path = 'pmnp_is_event_dataValue_update.xlsx'
eventDataValue_update_excel_file_path = 'eventDataValueUpdate.xlsx'
print( f"file_name . { eventDataValue_update_excel_file_path }" )
logging.info(f"file_name . { eventDataValue_update_excel_file_path }")

updateEventDataValues = pd.read_excel(eventDataValue_update_excel_file_path)
print( f"length of event. { len(updateEventDataValues) }" )
logging.info( f"length of event . { len(updateEventDataValues) }" )

'''
columns_of_interest = ['event', 'orgUnit', 'trackedEntityInstance', BeneficiaryRegID, 'eventDate','BenVisitID',
                       'VisitNo', 'AgeOnVisit', 'VisitReason', 'VisitCategory','ProvisionalDiagnosis',
                       'phyanthropometry_bmi', 'nurse_rbs','SystolicBP_1stReading','DiastolicBP_1stReading',
                       'PrescriptionID', 'ProcedureID', 'ProcedureName', 'TestResultValue']
'''                       
#data_of_interest = data[columns_of_interest]
'''
for index, eventDataValueRow in updateEventDataValues.iterrows():
    #print(f"Row {index + 1}: {row}" )
    
    updateEventDataValue = {
        "event": eventDataValueRow['event'],
        "program": eventDataValueRow['program'],
        "dataValues": [
            { "dataElement": eventDataValueRow['dataElement'], "value": eventDataValueRow['value'] }
        ]                 
    }

    update_eventDataValue_in_dhis2_xlsx(updateEventDataValue, eventDataValueRow['event'], eventDataValueRow['dataElement'], index + 2 )

'''


def update_eventDataValue_in_dhis2_xlsx(session, updateEventDataValue, eventUID, dataElementUid, row_no):

    #print( f" updateEventDataValue . { updateEventDataValue }" )
    event_update_url = f"{dhis2_api_url}events/{eventUID}/{dataElementUid}"
    #print( f"event_update_url . { event_update_url }" )
    # for IPPF CO BPR add verify=False,
    response = session.put(event_update_url, json=updateEventDataValue, verify=False, headers={"Content-Type": "application/json"})
    
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
        print(f"Events updated successfully. Row No : {row_no}. updated event : {eventUID}. impCount : {impCount} .updateCount : {updateCount} .ignoreCount : {ignoreCount}")
        logging.info(f"Events updated successfully. Row No : {row_no}. updated event : {eventUID}. impCount : {impCount} .updateCount : {updateCount} .ignoreCount : {ignoreCount}")
        #logging.info(f"Event created successfully . BenVisitID : {BenVisitID} . BeneficiaryRegID : {BeneficiaryRegID}. Event count: {event_count}. Event uid: {event_uid}" )
        #logging.info("MySQL connection closed")

    else:
        print(f"Failed to update events. Error: {response.text}")
        logging.error(f"Failed to update events. Row No : {row_no} .conflictsDetails : {conflictsDetails} .Status code: {response.status_code} .error details: {response.json()} .Error: {response.text}")


with ThreadPoolExecutor(max_workers=10) as executor:

    #print( f"length of event_list. { len(updateEventDataValues) }" )
    #logging.info( f"length of event_list . { len(updateEventDataValues) }" )
    for index, eventDataValueRow in updateEventDataValues.iterrows():
        #print(f"Row {index + 1}: {row}" )

        '''
        raw_value = eventDataValueRow['value']
        # ✅ Convert NaN → empty string (best for DHIS2)
        if pd.isna(raw_value) or raw_value is None:
            cleaned_value = ""
        else:
            cleaned_value = str(raw_value)
        '''
        updateEventDataValue = {
            "event": eventDataValueRow['event'],
            "program": eventDataValueRow['program'],
            "dataValues": [
                {
                    "dataElement": eventDataValueRow['dataElement'],
                    #"value": cleaned_value
                    "value": clean_dhis2_value(eventDataValueRow['value'])
                }
            ]
        }
        executor.submit(update_eventDataValue_in_dhis2_xlsx, session, updateEventDataValue, eventDataValueRow['event'], eventDataValueRow['dataElement'], index + 2)

current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"update eventDataValue finished . { current_time_end }" )
logging.info(f"update eventDataValue finished . { current_time_end }")

