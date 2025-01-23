#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
from dhis2_api_interaction import get_org_unit_data, get_tei_data, construct_xlsx_dataValueSet_payload, push_dataValueSet_in_dhis2_xlsx
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
dhis2_username = "*"
dhis2_password = "*"

from constants import LOG_FILE_EVENT_DATA_VALUE_UPDATE_MARTIAL_STATUS

# DHIS2 API credentials and URL
DHIS2_API_URL = "*"
DHIS2_AUTH = ("*", "*")

#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session = requests.Session()
session.auth = DHIS2_AUTH

logging.basicConfig(filename=LOG_FILE_EVENT_DATA_VALUE_UPDATE_MARTIAL_STATUS, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" update evenDataValue Marital status start . { current_time_start }" )
logging.info(f" update eventDataValue Marital status start . { current_time_start }")

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


def get_sqlview_data():
    
    # age_on_visit = P8cFNnfn9UP
    # sex = wGdLwfDzjyG
    # FSW type = GWdWZBnvv0G
    # Client of FSW type = CTAfO6mvhTl
    # Risk group = nQT7OA90MOq
    # Marital status = qYJQyXbZesE
    sql_view_url = f"{DHIS2_API_URL}sqlViews/qYJQyXbZesE/data?paging=false"

    #print(f"sql_view_url : {sql_view_url}")

    #response_sql_view = requests.get(sql_view_url,auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    
    response_sql_view = session.get(sql_view_url,auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    
    #print(f"response_sql_view : {response_sql_view.text}")

    if response_sql_view.status_code == 200:
        #print(f"response_sql_view : {response_sql_view.status_code}")
        response_sql_view_data = response_sql_view.json()
        #print(f"response_sql_view_data : {response_sql_view_data}")

        
        tempListGrid   = response_sql_view.json().get('listGrid', {})
        #print(f"tempListGrid : {tempListGrid}")
        #print(f"title : {tempListGrid.get('title')}")
        tempRows = tempListGrid.get('rows',[])

        if tempRows:
            for rows in tempRows:
                event = rows[0]
                dataValue = rows[1]
                #print(f"event : {event}, dataValue : {dataValue}")
                
        else:
            error_message = f"No data received for sqlview"
            print(error_message)

        #print(tempRows)

        
    else:
        print(f"Failed to retrieve sqlview data. Status code: {response_sql_view.status_code}")

    return tempRows


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


#eventDataValue_update_excel_file_path = 'hiv_event_dataValue_update.xlsx'
#print( f" file_name . { eventDataValue_update_excel_file_path }" )
#logging.info(f" file_name . { eventDataValue_update_excel_file_path }")
#updateEventDataValues = pd.read_excel(eventDataValue_update_excel_file_path)


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
    event_update_url = f"{DHIS2_API_URL}events/{eventUID}/{dataElementUid}"
    #print( f" event_update_url . { event_update_url }" )
    response = session.put(event_update_url, json=updateEventDataValue, headers={"Content-Type": "application/json"})
    
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
        logging.info(f"Events updated successfully. Row No {row_no}: . updated event : {eventUID}. impCount : {impCount} .updateCount : {updateCount} .ignoreCount : {ignoreCount}")
        #logging.info(f"Event created successfully . BenVisitID : {BenVisitID} . BeneficiaryRegID : {BeneficiaryRegID}. Event count: {event_count}. Event uid: {event_uid}" )
        #logging.info("MySQL connection closed")

    else:
        print(f"Failed to update events. Error: {response.text}")
        logging.error(f"Failed to update events. Row No {row_no} :  .conflictsDetails : {conflictsDetails} .Status code: {response.status_code} .error details: {response.json()} .Error: {response.text}")

with ThreadPoolExecutor(max_workers=10) as executor:
    # Create a session object for persistent connection
    
    sql_views_data = get_sqlview_data()
    print( f" length of event data value . { len(sql_views_data) }" )
    logging.info( f" length of event data value . { len(sql_views_data) }" )
    #for index, eventDataValueRow in updateEventDataValues.iterrows():
    for index, eventDataValue in enumerate(sql_views_data):
        #print(f"Row {index + 1}: {row}" )
    
        updateEventDataValue = {
            "program": eventDataValue[0],
            "event": eventDataValue[1],
            
            "dataValues": [
                { "dataElement": eventDataValue[2], "value": eventDataValue[3] }
            ]                 
        }

        executor.submit(update_eventDataValue_in_dhis2_xlsx, session, updateEventDataValue, eventDataValue[1], eventDataValue[2], index+1)

current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" update eventDataValue Marital status finished . { current_time_end }" )
logging.info(f" update eventDataValue Marital status finished . { current_time_end }")

