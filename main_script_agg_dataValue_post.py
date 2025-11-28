#import mysql_connection
#import dhis2_integration
from dhis2_api_interaction import get_orgunit_grp_member,get_aggregated_de_from_indicators, get_program_indicators_data_values, get_progral_indicators, push_dataValueSet_in_dhis2
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
print( f" pushing dataValue start . { current_time_start }" )
logging.info(f" pushing dataValue start . { current_time_start }")

tei_data_cache = {}
events_by_reg_id = {}


program_indicator_grp_members = get_progral_indicators()
orgunit_grp_members = get_orgunit_grp_member()
aggregated_de_dict = get_aggregated_de_from_indicators( )
program_indicators_data_values = get_program_indicators_data_values(program_indicator_grp_members, orgunit_grp_members)

print(f"aggregated_de_dict size {len(aggregated_de_dict)}")
print(f"program_indicators_data_values size {len(program_indicators_data_values)}")
logging.info(f"program_indicators_data_values size : {len(program_indicators_data_values)}")
#print(f"program_indicator_grp_members  {program_indicator_grp_members}")
#print(f"orgunit_grp_members  {program_indicator_grp_members}")

tempDataValues = list()
if program_indicators_data_values:
    for pi_dataValue in program_indicators_data_values:
        #print( f" pi_dataValue . { pi_dataValue }" )
        dataValue = {
            "dataElement": aggregated_de_dict[pi_dataValue['dataElement']].split("-")[0],
            "categoryOptionCombo": aggregated_de_dict[pi_dataValue['dataElement']].split("-")[1],
            "value": int(float(pi_dataValue['value'])),
            "period": pi_dataValue['period'],
            "orgUnit": pi_dataValue['orgUnit']
        }
        tempDataValues.append(dataValue)

    dataValueSet_payload = {
        "dataValues":tempDataValues
    }

    #print( f" dataValueSet_payload . { dataValueSet_payload }" )
    #print( f" dataValueSet_payload size . { len(dataValueSet_payload) }" )
    push_dataValueSet_in_dhis2( dataValueSet_payload)



current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" pushing dataValue finished . { current_time_end }" )
logging.info(f" pushing dataValue finished . { current_time_end }")

