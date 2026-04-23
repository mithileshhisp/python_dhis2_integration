#import mysql_connection
#import dhis2_integration
from dhis2_api_interaction import get_org_unit_data, get_tei_data, construct_xlsx_dataValueSet_payload, push_dataValueSet_in_dhis2
import database_connection
import logging, datetime
import pandas as pd
from database_connection import connect_to_mysql

import requests
import json
import numpy as np
import base64

from constants import LOG_FILE_DATA_VALUE_SET_DATA_SET_ATTRIBUTE

logging.basicConfig(filename=LOG_FILE_DATA_VALUE_SET_DATA_SET_ATTRIBUTE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


DHIS2_API_GET_POST_URL = "*******/api/"
DHIS2_AUTH_GET_POST = ("******", "******")


session_get_post = requests.Session()
session_get_post.auth = DHIS2_AUTH_GET_POST

org_unit_api_url = f"{DHIS2_API_GET_POST_URL}organisationUnits"
options_api_url = f"{DHIS2_API_GET_POST_URL}options"
enrollment_endpoint = f"{DHIS2_API_GET_POST_URL}trackedEntityInstances"
event_endpoint = f"{DHIS2_API_GET_POST_URL}events.json"


dataValueSet_endPoint = f"{DHIS2_API_GET_POST_URL}dataValueSets"


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"pushing dataValue start . { current_time_start }" )
logging.info(f"pushing dataValue start . { current_time_start }")


def push_dataValueSet_dataSetAttribute_in_dhis2(dataValueSet_payload):
    #print(f"dataValueSet_payload : {json.dumps(dataValueSet_payload)}")
    #logging.info(f"dataValueSet_payload : {json.dumps(dataValueSet_payload)}")

    response = session_get_post.post(
        dataValueSet_endPoint,
        data=json.dumps(dataValueSet_payload),
        headers={"Content-Type": "application/json"}
    )
    conflictsDetails = ""
    if response.status_code == 200:
        #print(f"DataValue created successfully.  Row No : {row_no} . orgUnit : {orgUnit} . response . {response.status_code}")
        #print(f"DataValue created successfully.  Row No : {row_no} . orgUnit : {orgUnit} . response . {response.json()}")

        conflictsDetails   = response.json().get("response", {}).get("conflicts")
        description   = response.json().get("response", {}).get("description")
        impCount = response.json().get("response", {}).get("importCount").get("imported")
        updateCount = response.json().get("response", {}).get("importCount").get("updated")
        ignoreCount = response.json().get("response", {}).get("importCount").get("ignored")
        
        print(f"DataValue created successfully. impCount : {impCount} . updateCount : {updateCount} . ignoreCount : {ignoreCount} . description : {description}")
        logging.info(f"DataValue created successfully. impCount : {impCount} . updateCount : {updateCount} . ignoreCount: {ignoreCount} . description : {description}")
        logging.info(f"DataValue created successfully : {response.text}")
    else:
        print(f"Failed to create dataValueSet. Error: {response.text}")
        logging.error(f"Failed to dataValueSet events . conflictsDetails : {conflictsDetails} . error details: {response.json()} .Error: {response.text}")


dataValueSet_excel_path = 'dataValueSetDataSetAttribute.xlsx' 
dataValueSet = pd.read_excel(dataValueSet_excel_path)
print( f"file_name . { dataValueSet_excel_path }" )
logging.info(f"file_name . { dataValueSet_excel_path }")
print( f"length of dataValueSet. { len(dataValueSet) }" )
logging.info( f"length of dataValueSet . { len(dataValueSet) }" )

#dataValues = []
tempDataValues = list()
for _, row in dataValueSet.iterrows():
        dataValue = {
            "dataElement": row['dataElementUID'],
            "categoryOptionCombo": row['categoryoptioncomboUID'],
            "attributeOptionCombo": row['attributeOptionComboUID'],
            "orgUnit": row['organisationunitUID'],
            "value": str(row['dataValue']),
            "period": str(row['isoPeriod']),
            "storedBy": str(row['storedBy'])
            #"created" : str(row['created']),
            #"lastUpdated" : str(row['lastUpdated'])
            
        }
        tempDataValues.append(dataValue)


dataValueSet_payload = {
    "dataValues":tempDataValues
}    

push_dataValueSet_dataSetAttribute_in_dhis2( dataValueSet_payload )

current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" pushing dataValue finished . { current_time_end }" )
logging.info(f" pushing dataValue finished . { current_time_end }")

