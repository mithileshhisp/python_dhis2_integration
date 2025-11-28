#import mysql_connection
#import dhis2_integration
from dhis2_api_interaction import get_org_unit_data, get_tei_data, construct_xlsx_dataValueSet_payload, push_dataValueSet_in_dhis2_xlsx
import database_connection
import logging, datetime
import pandas as pd
from database_connection import connect_to_mysql
import requests

from requests.auth import HTTPBasicAuth


from constants import LOG_FILE_DATA_VALUE_SET

logging.basicConfig(filename=LOG_FILE_DATA_VALUE_SET, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


DHIS2_API_GET_POST_URL = "*****/api/"
DHIS2_AUTH_GET_POST = ("****", "******")


session_get_post = requests.Session()
session_get_post.auth = DHIS2_AUTH_GET_POST



# logging.basicConfig(filename='bayer_event.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#mysql_connection = connect_to_mysql()
#mysql_conn = database_connection.establish_mysql_connection(mysql_host, mysql_port, mysql_user, mysql_password, mysql_database)

# logging.info("MySQL connection closed")

#print("Connected to MySQL database")
#logging.info("Connected to MySQL database")
#cursor = mysql_connection.cursor()

#results = database_connection.fetch_mysql_data(cursor)

#mysql_connection.close()

# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" pushing dataValue start . { current_time_start }" )
logging.info(f" pushing dataValue start . { current_time_start }")

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


#dataValueSet_excel_path = 'ippf_co_dataValueSet_import.xlsx' 

dataValueSet_excel_path = 'dataValueSet_import.xlsx' 
#dataValues = read_excel_to_dict(dataValueSet_excel_path)



#dataSetSource_excel_file_path = 'ippf_co_dataSet_source.xlsx'
#dataSetSource = pd.read_excel(dataSetSource_excel_file_path)

dataValueSetPeriod_excel_file_path = 'dataValueSet_period_list.xlsx'
dataValueSet_period_list = pd.read_excel(dataValueSetPeriod_excel_file_path)


print( f"file_name . { dataValueSet_excel_path }" )
logging.info(f"file_name . { dataValueSet_excel_path }")
print( f"file_name . { dataValueSetPeriod_excel_file_path }" )
logging.info(f"file_name . { dataValueSetPeriod_excel_file_path }")
print( f"length of periods. { len(dataValueSet_period_list) }" )
logging.info( f"length of periods . { len(dataValueSet_period_list) }" )

dataValueSet = pd.read_excel(dataValueSet_excel_path)
print( f"length of dataValueSet. { len(dataValueSet) }" )
logging.info( f"length of dataValueSet . { len(dataValueSet) }" )
                 
#data_of_interest = data[columns_of_interest]

for index, sourceRow in dataValueSet_period_list.iterrows():
    #print(f"Row {index + 1}: {row}" )
    
    #row['event'],row['orgUnit'],row['trackedEntityInstance'],
    #dataValueSet_payload = construct_xlsx_dataValueSet_payload(dataValues,row['orguid'])
    tempIsoPeriod = sourceRow['isoPeriod']
    
    #dataValues = []
    tempDataValues = list()
    #option_dict = {}

    for _, row in dataValueSet.iterrows():
        dataValue = {
            "dataElement": str(row['dataElementUID']),
            "categoryOptionCombo": str(row['categoryoptioncomboUID']),
            "value": str(row['dataValue']),
            "period": str(tempIsoPeriod),
            "orgUnit": str(row['organisationunitUID']),
            #"orgUnit": tempOrgUnit,
        }
        tempDataValues.append(dataValue)
    
    dataValueSet_payload = {
        "dataValues":tempDataValues
    }    


    #print(f" Row {index + 2} .. {row['BeneficiaryRegID']}  ")
    #logging.info(f" Row {index + 2} .. {row['BeneficiaryRegID']}  ")

    #logging.info(f" pushing event BeneficiaryRegID . {row['BeneficiaryRegID']} ")
    #for col in columns_of_interest:
        #print(f"  {col}: {row[col]}")
    
    push_dataValueSet_in_dhis2_xlsx( session_get_post, dataValueSet_payload, tempIsoPeriod, index + 2 )
    #push_dataValueSet_in_dhis2_xlsx( dataValueSet_payload, tempOrgUnit, index + 2 )


current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" pushing dataValue finished . { current_time_end }" )
logging.info(f" pushing dataValue finished . { current_time_end }")

