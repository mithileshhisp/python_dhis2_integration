#import mysql_connection
#import dhis2_integration
from dhis2_api_interaction import get_org_unit_data, get_tei_data, construct_xlsx_dataValueSet_payload, push_dataValueSet_in_dhis2_xlsx
import database_connection
import logging, datetime
import pandas as pd
from database_connection import connect_to_mysql
import requests
import json

from requests.auth import HTTPBasicAuth


from constants import LOG_FILE_DATA_VALUE_SET_DELETE

logging.basicConfig(filename=LOG_FILE_DATA_VALUE_SET_DELETE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


DHIS2_API_GET_POST_URL = "https://mm.dhis2.net/hmis/api/"
DHIS2_AUTH_GET_POST = ("****", "*****")

dataValueSet_endPoint = f"{DHIS2_API_GET_POST_URL}dataValues"
session_get_post = requests.Session()
session_get_post.auth = DHIS2_AUTH_GET_POST


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Deleting dataValue start . { current_time_start }" )
logging.info(f"Deleting dataValue start . { current_time_start }")



def delete_dataValueSet_in_dhis2_xlsx(session_get_post, dataValueSet_payload, tempOrgUnit, row_no):
    
    '''
    response = session_get_post.post(
        dataValueSet_endPoint,
        dataValueSet_payload,
        headers={"Content-Type": "application/json"}
    )
    '''
    #print(f" dataValueSet_endPoint. : {dataValueSet_endPoint}")
    #print(f" dataValueSet_payload. : {dataValueSet_payload}")
    response = session_get_post.delete(dataValueSet_endPoint, params=dataValueSet_payload)

    if response.status_code in (200, 204):
        #print(f"DataValue created successfully.  Row No : {row_no} . orgUnit : {orgUnit} . response . {response.status_code}")
        #print(f"DataValue created successfully.  Row No : {row_no} . orgUnit : {orgUnit} . response . {response.json()}")

        #print(f" Respopnse dataValueSet. : {response.text}")

        print(f"DataValue Deleted successfully. Row No : {row_no} . tempOrgUnit : {tempOrgUnit}")
        logging.info(f"DataValue Deleted successfully. Row No : {row_no} . tempOrgUnit : {tempOrgUnit} ")
        
    else:
        print(f"Failed to delete dataValueSet. Error: {response.text} , {response.status_code}")
        logging.error(f"Failed to delete dataValueSet Error. Row No : {row_no} . tempOrgUnit : {tempOrgUnit} .  Status code: {response.status_code} .Error: {response.text}")



#dataValueSet_excel_path = 'ippf_co_dataValueSet_import.xlsx' 

dataValueSet_delete_excel_path = 'dataValueSet_delete_dataSet_attribute.xlsx' 
#dataValues = read_excel_to_dict(dataValueSet_excel_path)

print( f"file_name . { dataValueSet_delete_excel_path }" )
logging.info(f"file_name . { dataValueSet_delete_excel_path }")

dataValueSet_delete = pd.read_excel(dataValueSet_delete_excel_path)
print( f"length of dataValueSet. { len(dataValueSet_delete) }" )
logging.info( f"length of dataValueSet . { len(dataValueSet_delete) }" )
                 
#data_of_interest = data[columns_of_interest]

for index, row in dataValueSet_delete.iterrows():
    dataValueDelete = { 
        "de": row['dataElementUID'],
        "co": row['categoryoptioncomboUID'],
        "ds": row['dataSetUID'],
        "ou": row['organisationunitUID'],
        "pe": str(row['isoPeriod'])
        
    }
    delete_dataValueSet_in_dhis2_xlsx( session_get_post, dataValueDelete, row['organisationunitUID'], index + 2 )
    
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Deleting dataValue finished . { current_time_end }" )
logging.info(f"Deleting dataValue finished . { current_time_end }")

