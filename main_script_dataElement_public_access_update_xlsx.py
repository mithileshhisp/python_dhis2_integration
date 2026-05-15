# optionSet sharing-setting update DHIS2 2.41

import pandas as pd
import requests
import json
import logging, datetime
import os

from constants import LOG_FILE_DATAELEMENT_PUBLIC_ACCESS_UPDATE
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log filename
#log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = LOG_FILE_DATAELEMENT_PUBLIC_ACCESS_UPDATE
#log_filename = f"{LOG_FILE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(LOG_DIR, log_filename)
logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# ==========================================
# CONFIGURATION
# ==========================================
BASE_URL = "********"
USERNAME = "******"
PASSWORD = "******"

EXCEL_FILE = "dataElementPublicAccessUpdate.xlsx"
SHEET_NAME = "dataElementPublicAccessUpdate"

# ==========================================
# CREATE SESSION
# ==========================================
session = requests.Session()
session.auth = (USERNAME, PASSWORD)

session.headers.update({
    "Content-Type": "application/json"
})

# ==========================================
# READ EXCEL
# ==========================================
df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"DataElement Public Access Update start at. { current_time_start }" )
logging.info(f"DataElement Public Access Update start at. { current_time_start }")

df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

df = df.where(pd.notnull(df), None)

records = df.to_dict(orient="records")

print(f"Total rows in Excel: {len(records)}")
logging.info(f"Total rows in Excel: {len(records)}")

import_count = 1
update = 0
failed = 0
skipped = 0

# ==========================================
# LOOP THROUGH ROWS
# ==========================================
for index, row in df.iterrows():

    import_count += 1

    try:
        data_element_uid = row["uid"]
        public_access = row["publicAccess"]

        # ==========================================
        # GET DATA ELEMENT
        # ==========================================
        get_url = f"{BASE_URL}/api/dataElements/{data_element_uid}.json?paging=false"

        get_response = session.get(get_url)
        #print(get_response.status_code)
        #print(get_response.text)

        if get_response.status_code != 200:
            print(
                f"Row - {import_count} GET error: "
                f"{get_response.status_code} - {get_response.text}"
            )
            logging.info(
                f'Row - {import_count} GET error: '
                f'{get_response.status_code} - {get_response.text}'
            )
            skipped += 1
            continue

        update_data_element = get_response.json()

        # ==========================================
        # UPDATE SHARING PUBLIC ACCESS
        # ==========================================
        update_data_element["id"] = data_element_uid

        if "sharing" not in update_data_element:
            update_data_element["sharing"] = {}

        update_data_element["sharing"]["public"] = public_access

        # ==========================================
        # PUT UPDATED DATA ELEMENT
        # ==========================================
        put_url = f"{BASE_URL}/api/dataElements/{data_element_uid}"

        put_response = session.put(
            put_url,
            data=json.dumps(update_data_element)
        )

        if put_response.status_code in [200, 201]:
            print(
                f"Row - {import_count} update done response: "
                f"{put_response.text}"
            )
            logging.info(
                f"Row - {import_count} update done response: "
                f"{put_response.text}"
            )
            update += 1
        else:
            print(
                f"Row - {import_count} error response: "
                f"{put_response.status_code} - {put_response.text}"
            )
            logging.info(
                f"Row - {import_count} error response: "
                f"{put_response.status_code} - {put_response.text}"
            )
            failed += 1

    except Exception as e:
        print(f"Row - {import_count} Exception: {str(e)}")

    print("-" * 50)
    logging.info("-" * 50)
# ==========================================
# COMPLETE
# ==========================================
print("Update complete")


# -------------------------------
# DHIS2 Import Summary
# -------------------------------
print("\n========== DHIS2 IMPORT SUMMARY ==========")
logging.info(f"\n========== DHIS2 IMPORT SUMMARY ==========")
print(f"Total Records : {len(records)}")
logging.info(f"Total Records : {len(records)}")
print(f"Updated       : {update}")
logging.info(f"Updated       : {update}")
print(f"Skipped       : {skipped}")
logging.info(f"Skipped       : {skipped}")
print(f"Failed        : {failed}")
logging.info(f"Failed        : {failed}")
print("==========================================")
logging.info("==========================================")

current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"DataElement Public Access Update end at. { current_time_end }" )
logging.info(f"DataElement Public Access Update end at. { current_time_end }")