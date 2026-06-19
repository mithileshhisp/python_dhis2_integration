import pandas as pd
import requests
import json
import logging, datetime
import os

from constants import LOG_FILE_EVENT_DATAVALUE_MULTIPLE_DE

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log filename
#log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = LOG_FILE_EVENT_DATAVALUE_MULTIPLE_DE
#log_filename = f"{LOG_FILE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# =========================
# CONFIGURATION
# =========================

current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Event Update for multiple dataelement start at. { current_time_start }" )
logging.info(f"Event Update for multiple dataelement start at. { current_time_start }")




DHIS2_API_POST_URL =  "https://links.hispindia.org/ippf_uin/api/" ### training
DHIS2_AUTH_POST = ("******", "*******")

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST
session_post.headers.update({
    "Accept": "application/json",
    "Content-Type": "application/json"
})


EXCEL_FILE = "eventDataValuesUpdate.xlsx"
SHEET_NAME = "eventDataValuesUpdate"

# =========================
# READ EXCEL FILE
# =========================

# First row automatically becomes header
df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

#df = pd.read_excel("user_tei_search_orgunits_update.xlsx", sheet_name="user_tei_search_orgunits_update")
# Convert NaN → None
df = df.where(pd.notnull(df), None)

records = df.to_dict(orient="records")

print(f"Total Event rows in Excel: {len(records)}")
logging.info(f"Total Event rows in Excel: {len(records)}")

success = 0
failed = 0
skipped = 0

# Convert dataframe to list of dicts
xl_row_object = df.to_dict(orient="records")

# Get column names
object_keys = list(df.columns)

import_count = 1
success = 0
failed = 0
skipped = 0

# =========================
# LOOP THROUGH EACH ROW
# =========================

for row_no, row in enumerate(xl_row_object, start=1):

    try:

        print(f"\nProcessing Row: {row_no}")

        # ---------------------------------
        # EVENT UID AND PROGRAM UID
        # ---------------------------------

        event_uid = str(row[object_keys[0]]).strip()
        program_uid = str(row[object_keys[1]]).strip()

        # ---------------------------------
        # GET EXISTING EVENT
        # ---------------------------------

        get_url = f"{DHIS2_API_POST_URL}events/{event_uid}.json?paging=false"
        #print("GET get_url:", get_url)
        response = session_post.get(get_url)

        #print("GET Status:", response.status_code)

        if response.status_code != 200:
            print(f"Error getting event {event_uid}")
            print(response.text)
            failed += 1
            continue

        # Safe JSON parsing
        try:
            event_response = response.json()
        except Exception as json_error:
            print(f"JSON Parse Error for event {event_uid}")
            print(response.text)
            failed += 1
            continue

        #print(f"Row {row_no}: event_response → {event_response}")

        # Existing data values
        #event_data_values = event_response.get("dataValues", [])

        # ---------------------------------
        # ADD NEW DATA VALUES
        # ---------------------------------

        '''
        for col_index in range(2, len(object_keys)):

            data_element = object_keys[col_index].strip()

            value = row.get(object_keys[col_index])

            # Skip NaN, None, empty string
            if (
                pd.notna(value)
                and value is not None
                and str(value).strip() != ""
            ):

                event_data_value = {
                    "dataElement": data_element,
                    "value": str(value).strip()
                }

                # IMPORTANT:
                # append INSIDE if block
                event_data_values.append(event_data_value)

            '''
        # ---------------------------------
        # EXISTING DATA VALUES
        # ---------------------------------

        event_data_values = event_response.get("dataValues", [])

        # Convert existing dataValues to dictionary
        existing_values = {}

        for dv in event_data_values:
            existing_values[dv["dataElement"]] = dv.get("value")

        # ---------------------------------
        # UPDATE / ADD DATA VALUES
        # ---------------------------------

        for col_index in range(2, len(object_keys)):

            data_element = object_keys[col_index].strip()

            value = row.get(object_keys[col_index])

            # Skip NaN, None, empty
            if (
                pd.notna(value)
                and value is not None
                and str(value).strip() != ""
            ):

                # Update existing value
                existing_values[data_element] = str(value).strip()

            # ---------------------------------
            # CONVERT BACK TO DHIS2 FORMAT
            # ---------------------------------

            event_data_values = []

            for de, val in existing_values.items():

                event_data_values.append({
                    "dataElement": de,
                    "value": val
                })


        # ---------------------------------
        # CREATE UPDATE PAYLOAD
        # ---------------------------------

        update_event_data_values = {
            "event": event_uid,
            "program": program_uid,
            "dataValues": event_data_values
        }

        #print(f"Row {row_no}: Event payload → {update_event_data_values}")

        # ---------------------------------
        # UPDATE EVENT
        # ---------------------------------

        put_url = f"{DHIS2_API_POST_URL}events/{event_uid}"

        update_response = session_post.put(
            put_url,
            headers={
                "Content-Type": "application/json"
            },
            json=update_event_data_values
        )

        #print("PUT Status:", update_response.status_code)

        if update_response.status_code in [200, 201, 204]:

            print(f"Row {row_no}: Event Updated success → {event_uid}")

            logging.info(
                f"Row {row_no}: Event Updated success : {event_uid}"
            )

            success += 1

        else:

            print(f"Event NOT updated: {event_uid}")
            print(update_response.text)

            logging.error(
                f"Row {row_no}: Failed to update Event "
                f"{event_uid} : {update_response.text}"
            )

            failed += 1

    except Exception as e:

        print(f"Error processing row {row_no}")
        print(f"Row Data: {row}")
        print(str(e))

        logging.exception(f"Error processing row {row_no}")

        failed += 1

    print("-" * 50)
    logging.info("-" * 50)

    import_count += 1

print("Update done")

# -------------------------------
# DHIS2 Import Summary
# -------------------------------
print("\n========== DHIS2 IMPORT SUMMARY ==========")
logging.info(f"\n========== DHIS2 IMPORT SUMMARY ==========")
print(f"Total Records : {len(records)}")
logging.info(f"Total Records : {len(records)}")
print(f"Updated       : {success}")
logging.info(f"Updated       : {success}")
print(f"Skipped       : {skipped}")
logging.info(f"Skipped       : {skipped}")
print(f"Failed        : {failed}")
logging.info(f"Failed        : {failed}")
print("==========================================")
logging.info("==========================================")

current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Event Update for multiple dataelement end at. { current_time_end }" )
logging.info(f"Event Update for multiple dataelement end at. { current_time_end }")


'''
import pandas as pd
import requests
import json

BASE_URL = "https://your-dhis2-instance/api"
USERNAME = "admin"
PASSWORD = "district"

EXCEL_FILE = "eventDataValuesUpdate.xlsx"
SHEET_NAME = "eventDataValuesUpdate"

df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

xl_row_object = df.to_dict(orient="records")

object_keys = list(df.columns)

import_count = 1

for row in xl_row_object:

    try:

        event_uid = str(row[object_keys[0]]).strip()
        program_uid = str(row[object_keys[1]]).strip()

        print(f"\nProcessing Event: {event_uid}")

        # ==========================================
        # GET EVENT
        # ==========================================

        get_url = f"{BASE_URL}/events/{event_uid}.json"

        response = requests.get(
            get_url,
            auth=(USERNAME, PASSWORD),
            headers={
                "Accept": "application/json"
            }
        )

        print("GET Status:", response.status_code)

        # Print raw response if error
        if response.status_code != 200:
            print("GET ERROR RESPONSE:")
            print(response.text)
            continue

        # Safe JSON parsing
        try:
            event_response = response.json()
        except Exception as json_error:
            print("JSON Parse Error")
            print(response.text)
            continue

        # ==========================================
        # EXISTING DATA VALUES
        # ==========================================

        event_data_values = event_response.get("dataValues", [])

        # ==========================================
        # ADD NEW DATA VALUES
        # ==========================================

        for i in range(2, len(object_keys)):

            data_element = object_keys[i].strip()

            value = row.get(object_keys[i])

            # Skip null/empty values
            if pd.notna(value) and value != "":

                event_data_value = {
                    "dataElement": data_element,
                    "value": str(value)
                }

                event_data_values.append(event_data_value)

        # ==========================================
        # UPDATE PAYLOAD
        # ==========================================

        update_payload = {
            "event": event_uid,
            "program": program_uid,
            "dataValues": event_data_values
        }

        print(json.dumps(update_payload, indent=2))

        # ==========================================
        # UPDATE EVENT
        # ==========================================

        put_url = f"{BASE_URL}/events/{event_uid}"

        update_response = requests.put(
            put_url,
            auth=(USERNAME, PASSWORD),
            headers={
                "Content-Type": "application/json"
            },
            json=update_payload
        )

        print("PUT Status:", update_response.status_code)
        print(update_response.text)

    except Exception as e:
        print(f"Error processing row: {row}")
        print(str(e))

    import_count += 1

print("Update done")

'''