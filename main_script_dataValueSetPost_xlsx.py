#import mysql_connection
#import dhis2_integration
from dhis2_api_interaction import get_org_unit_data, get_tei_data, construct_xlsx_dataValueSet_payload, push_dataValueSet_in_dhis2
import database_connection
import logging, datetime
import pandas as pd
from database_connection import connect_to_mysql


from constants import LOG_FILE_DATA_VALUE_SET

logging.basicConfig(filename=LOG_FILE_DATA_VALUE_SET, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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
print( f"pushing dataValue start . { current_time_start }" )
logging.info(f"pushing dataValue start . { current_time_start }")

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

dataValueSet_excel_path = 'dataValueSet_who_population_child_adult_15Sept2025.xlsx' 
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
            #"attributeOptionCombo": row['attributeOptionComboUID'],
            "orgUnit": row['organisationunitUID'],
            "value": str(row['dataValue']),
            "period": str(row['isoPeriod']),
            #"storedBy": row['storedBy'],
            
        }
        tempDataValues.append(dataValue)


dataValueSet_payload = {
    "dataValues":tempDataValues
}    

push_dataValueSet_in_dhis2( dataValueSet_payload )


current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" pushing dataValue finished . { current_time_end }" )
logging.info(f" pushing dataValue finished . { current_time_end }")

