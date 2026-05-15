# Translation Update Script in Python

# Read and process multiple sheets from one Excel file

import pandas as pd
import requests

import json
import logging, datetime
import os

from constants import LOG_FILE_TRANSLATION_UPDATE
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log filename
#log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = LOG_FILE_TRANSLATION_UPDATE
#log_filename = f"{LOG_FILE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(LOG_DIR, log_filename)
logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# ==========================================
# CONFIGURATION
# ==========================================
BASE_URL = "********"
USERNAME = "******"
PASSWORD = "******"

EXCEL_FILE = "translation_update.xlsx"

# ==========================================
# CREATE SESSION
# ==========================================
session = requests.Session()
session.auth = (USERNAME, PASSWORD)

session.headers.update({
    "Content-Type": "application/json"
})

# ==========================================
# GET ALL SHEET NAMES
# ==========================================
excel_file = pd.ExcelFile(EXCEL_FILE)

sheet_names = excel_file.sheet_names

#print("Sheets found:")
#print(sheet_names)

print( f"Sheets found sheet_names: {sheet_names}" )
logging.info(f"Sheets found sheet_names: {sheet_names}" )

current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Translation Update start at. { current_time_start }" )
logging.info(f"Translation Update start at. { current_time_start }")




# ==========================================
# LOOP THROUGH ALL SHEETS
# ==========================================
for sheet_name in sheet_names:

    print("\n================================================")
    print(f"Processing Sheet: {sheet_name}")
    logging.info(f"Processing Sheet: {sheet_name}")
    print("================================================")

    #df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)

    try:

        # ==========================================
        # READ CURRENT SHEET
        # ==========================================
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)

        df = df.where(pd.notnull(df), None)

        records = df.to_dict(orient="records")

        print(f"Total rows in sheet {sheet_name} : {len(records)}")
        logging.info(f"Total rows in sheet {sheet_name} : {len(records)}")

        # Skip empty sheets
        if df.empty:
            print(f"Sheet '{sheet_name}' is empty")
            logging.info(f"Sheet '{sheet_name}' is empty")
            continue

        # ==========================================
        # GROUP ROWS BY ID
        # ==========================================
        total_rows = {}

        first_column = df.columns[0]

        for _, row in df.iterrows():

            object_id = row[first_column]

            if pd.isna(object_id):
                continue

            if object_id not in total_rows:
                total_rows[object_id] = []

            obj = {}

            for column in df.columns[1:]:

                value = row[column]

                if pd.isna(value):
                    value = ""

                obj[column] = value

            total_rows[object_id].append(obj)

        ids = list(total_rows.keys())

        print(f"Total IDs in sheet '{sheet_name}': {len(ids)}")
        logging.info(f"Total IDs in sheet '{sheet_name}': {len(ids)}")
        # ==========================================
        # PROCESS EACH ID
        # ==========================================
        for object_id in ids:

            try:

                url = f"{BASE_URL}/{sheet_name}/{object_id}.json?paging=false"

                # ==========================================
                # GET OBJECT
                # ==========================================
                response = session.get(url)

                if response.status_code != 200:
                    print(
                        f"[ERROR] GET failed for ID: {object_id}"
                    )
                    print(response.status_code)
                    print(response.text)
                    print(f"Get response '{response.status_code}' : {response.text}")
                    logging.info(f"Get response '{response.status_code}' : {response.text}")
                    continue

                data = response.json()

                translations = data.get("translations", [])
                translation_arr = translations.copy()

                check_data = False

                # ==========================================
                # PROCESS TRANSLATIONS
                # ==========================================
                for row in total_rows[object_id]:

                    check_arr = True

                    for index, translation in enumerate(translations):

                        # UPDATE EXISTING
                        if (
                            translation.get("property") == row.get("property")
                            and translation.get("locale") == row.get("locale")
                            and translation.get("value") != row.get("value")
                        ):

                            translation_arr[index]["value"] = row.get("value")

                            check_arr = False
                            check_data = True

                            print(
                                f"[UPDATED] Sheet: {sheet_name} "
                                f"ID: {object_id}"
                            )
                            logging.info( f"[UPDATED] Sheet: {sheet_name} "
                                f"ID: {object_id}"
                            )
                        
                        # SAME VALUE
                        elif (
                            translation.get("property") == row.get("property")
                            and translation.get("locale") == row.get("locale")
                            and translation.get("value") == row.get("value")
                        ):

                            check_arr = False

                    # ADD NEW TRANSLATION
                    if check_arr:

                        translation_arr.append({
                            "property": row.get("property"),
                            "locale": row.get("locale"),
                            "value": row.get("value")
                        })

                        check_data = True

                        print(
                            f"[ADDED] Sheet: {sheet_name} "
                            f"ID: {object_id}"
                        )
                        logging.info( 
                            f"[ADDED] Sheet: {sheet_name} "
                            f"ID: {object_id}"
                        )

                # ==========================================
                # UPDATE OBJECT
                # ==========================================
                if check_data:

                    data["translations"] = translation_arr

                    put_response = session.put(
                        url,
                        data=json.dumps(data)
                    )

                    if put_response.status_code in [200, 201]:
                        print(
                            f"[SUCCESS] Updated "
                            f"Sheet: {sheet_name} "
                            f"ID: {object_id}"
                            f"{put_response.text}"
                        )
                        logging.info( 
                            f"[SUCCESS] Updated "
                            f"Sheet: {sheet_name} "
                            f"ID: {object_id}"
                            f"{put_response.text}"
                        )
                    else:
                        print(
                            f"[ERROR] PUT failed "
                            f"Sheet: {sheet_name} "
                            f"ID: {object_id} error : {put_response.text}" 
                        )
                        logging.info( 
                            f"[ERROR] PUT failed "
                            f"Sheet: {sheet_name} "
                            f"ID: {object_id} error : {put_response.text}"
                        )

                        #print(put_response.text)
                        
                else:
                    print(
                        f"[NO CHANGE] Sheet: {sheet_name} "
                        f"ID: {object_id} "
                        f"Translations Property: {translation.get('property')} "
                        f"Translations Locale: {translation.get('locale')} "
                        f"Translations Value: {translation.get('value')} "
                    )
                    logging.info( 
                        f"[NO CHANGE] Sheet: {sheet_name} "
                        f"ID: {object_id}"
                        f"Translations Property: {translation.get('property')} "
                        f"Translations Locale: {translation.get('locale')} "
                        f"Translations Value: {translation.get('value')} "

                        #f"Translations: {translation_arr}"
                    )

            except Exception as e:
                print(
                    f"[EXCEPTION] Sheet: {sheet_name} "
                    f"ID: {object_id}"
                )
                logging.info( 
                    f"[EXCEPTION] Sheet: {sheet_name} "
                    f"ID: {object_id}"
                )
                print(str(e))

    except Exception as e:
        print(f"[SHEET ERROR] {sheet_name} : str(e)")
        logging.info(f"[SHEET ERROR] {sheet_name} : str(e) ")
        #print(str(e))

    print("-" * 50)
    logging.info("-" * 50)

print("\nAll sheets processed successfully")


# -------------------------------
# DHIS2 Import Summary
# -------------------------------
print("\n========== DHIS2 IMPORT SUMMARY ==========")
logging.info(f"\n========== DHIS2 IMPORT SUMMARY ==========")


current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"Translation Update end at. { current_time_end }" )
logging.info(f"Translation Update end at. { current_time_end }")