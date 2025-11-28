# main_script.py

# Author: mithilesh
import logging
# import pandas as pd
from datetime import date, timedelta,datetime
from concurrent.futures import ThreadPoolExecutor
from dhis2_api_interaction import get_org_unit_data, push_dataValueSet_in_dhis2
from database_connection import connect_to_mysql

from constants import LOG_FILE_DATA_VALUE_SET_LAST_SYNC

logging.basicConfig(filename=LOG_FILE_DATA_VALUE_SET_LAST_SYNC, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# logging.basicConfig(filename='104_enrollment.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

num_threads = 20

def assign_value_if_not_null(value):
    if value is not None and value != "null":
        return value
    else:
        return ""
tempDataValues = list()
def push_to_dataValue_last_sync_date_for_row(row):
    
    VanName, VanID, FacilityName, CreatedDate = row

    last_sync_date_dataValue = CreatedDate.strftime("%Y-%m-%d %H:%M:%S")

    # org_unit_id, option_name = get_org_unit_and_option_data(PermSubDistrictId, PermVillageId)
    org_unit_id = get_org_unit_data(VanID)

    dataValue = {
            "dataElement": "FIWQ6T7ZjVs",
            "categoryOptionCombo": "HllvX50cXC0",
            "value": last_sync_date_dataValue,
            "period": datetime.now().strftime("%Y"),
            "orgUnit": org_unit_id
        }
    tempDataValues.append(dataValue)

try:

    mysql_connection = connect_to_mysql()

    if mysql_connection.is_connected():
        logging.info("STFC MMU Last_Sync_Date query")
        # Get the current date and time
        current_time_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print( f" pushing Last_Sync_Date start . { current_time_start }" )
        logging.info(f" pushing Last_Sync_Date start . { current_time_start }")
        # Returns the current local date
        today = date.today()
        todayStartDate = today.strftime("%Y-%m-%d") + " " + "00:00:00"
        oneDayBeforeToday = today - timedelta(days=1)
        oneDayBeforeTodayStartDate = oneDayBeforeToday.strftime("%Y-%m-%d") + " " + "00:00:00"
        oneDayBeforeTodayEndDate = oneDayBeforeToday.strftime("%Y-%m-%d") + " " + "23:59:59"
        todayEndDate = today.strftime("%Y-%m-%d") + " " + "23:59:59"
        #print(f"oneDayBeforeTodayStartDate {oneDayBeforeTodayStartDate}", f"todayEnd : {todayEndDate}")
        #logging.info(f"oneDayBeforeTodayStartDate {oneDayBeforeTodayStartDate}. todayEnd : {todayEndDate}")
        #print("Today date is: ", todayStart )

        print("STFC Last_Sync_Date db enrollment query") 
        print("Connected to MySQL database")
        #print("Today date is: ", todayStart )
        print("STFC Last_Sync_Date db enrollment query") 
        print("Connected to MySQL database")
        logging.info("Connected to MySQL database")
        mysql_cursor = mysql_connection.cursor()
        mysql_query = f"""

        SELECT m.VanName, m.VanID, f.FacilityName, max(t.CreatedDate) As Last_Sync_Date 
        from db_iemr.t_benvisitdetail t
        INNER JOIN db_iemr.m_van m on m.vanid=t.vanid
        INNER JOIN db_iemr.m_facility f on f.FacilityID=m.FacilityID
        group by m.VanName;

        """
        mysql_cursor.execute(mysql_query)
        mysql_rows = mysql_cursor.fetchall()
        logging.info(f"mysql_rows size {len(mysql_rows)}")
        print(f"mysql_rows size {len(mysql_rows)}")

        #for row in mysql_rows:
            #print(f"mysql_rows {row}")
            #create_enrollment_for_row(row)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for row in mysql_rows:
                #print(f"mysql_rows {row}")
                executor.submit(push_to_dataValue_last_sync_date_for_row, row)

    dataValueSet_payload = {
        "dataValues":tempDataValues
    }                

    push_dataValueSet_in_dhis2( dataValueSet_payload )

except Exception as e:
    logging.error(f"Error: {str(e)}")
finally:
    if 'mysql_cursor' in locals():
        mysql_cursor.close()
    if 'mysql_connection' in locals() and mysql_connection.is_connected():
        mysql_connection.close()
        current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print( f"pushing Last_Sync_Date finished . { current_time_end }" )
        logging.info(f"pushing Last_Sync_Date finished . { current_time_end }")
        logging.info("MySQL connection closed")



#i_ben_mapping.CreatedDate between '{oneDayBeforeTodayStartDate}' and '{oneDayBeforeTodayEndDate}'
#i_ben_mapping.CreatedDate between '{oneDayBeforeTodayStartDate}' and '{todayEndDate}'
#i_ben_mapping.CreatedDate between  '2024-06-20 00:00:00' and '2024-06-25 00:00:00'