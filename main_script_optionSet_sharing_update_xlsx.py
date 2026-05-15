# optionSet sharing-setting update

import pandas as pd
import requests
import json
import logging, datetime
import os

from constants import LOG_FILE_OPTIONSET_SHATING_UPDATE
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log filename
#log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = LOG_FILE_OPTIONSET_SHATING_UPDATE
#log_filename = f"{LOG_FILE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(LOG_DIR, log_filename)
logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# =========================
# CONFIGURATION
# =========================
BASE_URL = "********"
USERNAME = "******"
PASSWORD = "******"

EXCEL_FILE = "optionSetsSharingPost.xlsx"
SHEET_NAME = "optionSetSharingPost"

# =========================
# READ EXCEL SHEET
# =========================

current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"OptionSet Sharing Update start at. { current_time_start }" )
logging.info(f"OptionSet Sharing Update start at. { current_time_start }")

df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

df = df.where(pd.notnull(df), None)

records = df.to_dict(orient="records")

print(f"Total rows in Excel: {len(records)}")
logging.info(f"Total rows in Excel: {len(records)}")

session = requests.Session()
session.auth = (USERNAME, PASSWORD)
session.headers.update({
    "Content-Type": "application/json"
})

import_count = 1
update = 0
failed = 0
skipped = 0

for index, row in df.iterrows():

    import_count += 1

    try:
        option_set_uid = row["uid"]
        public_access = row["publicAccess"]

        # ==========================================
        # GET EXISTING SHARING SETTINGS
        # ==========================================
        get_url = f"{BASE_URL}/api/sharing.json?type=optionSet&id={option_set_uid}"

        get_response = session.get(get_url)

        if get_response.status_code != 200:
            print(
                f'Row - {import_count} GET error: '
                f'{get_response.status_code} - {get_response.text}'
            )
            logging.info(
                f'Row - {import_count} GET error: '
                f'{get_response.status_code} - {get_response.text}'
            )
            skipped += 1
            continue

        option_set_response = get_response.json()

        # ==========================================
        # PREPARE SHARING PAYLOAD
        # ==========================================
        sharing_payload = {
            "allowPublicAccess": option_set_response.get("allowPublicAccess"),
            "allowExternalAccess": option_set_response.get("allowExternalAccess"),
            "object": {
                "id": option_set_response["object"]["id"],
                "name": option_set_response["object"]["name"],
                "displayName": option_set_response["object"]["displayName"],
                "user": option_set_response["object"].get("user"),
                "userGroupAccesses": option_set_response["object"].get("userGroupAccesses", []),
                "userAccesses": option_set_response["object"].get("userAccesses", []),
                "externalAccess": option_set_response["object"].get("externalAccess"),
                "publicAccess": public_access
            }
        }

        # ==========================================
        # POST UPDATED SHARING SETTINGS
        # ==========================================
        post_url = f"{BASE_URL}/api/sharing.json?type=optionSet&id={option_set_uid}"

        post_response = session.post(
            post_url,
            data=json.dumps(sharing_payload)
        )

        if post_response.status_code in [200, 201]:
            print(
                f"Row - {import_count} update done response: "
                f"{post_response.text}"
            )
            logging.info(
                f"Row - {import_count} update done response: "
                f"{post_response.text}"
            )
            update += 1
        else:
            print(
                f"Row - {import_count} error response: "
                f"{post_response.status_code} - {post_response.text}"
            )
            logging.info(
                f"Row - {import_count} error response: "
                f"{post_response.status_code} - {post_response.text}"
            )
            failed += 1

    except Exception as e:
        print(f"Row - {import_count} Exception: {str(e)}")

    print("-" * 50)
    logging.info("-" * 50)
# =========================
# COMPLETE MESSAGE
# =========================
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
print( f"OptionSet Sharing Update end at. { current_time_end }" )
logging.info(f"OptionSet Sharing Update end at. { current_time_end }")

