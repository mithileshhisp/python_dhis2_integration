#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
import os

from constants import LOG_FILE_USERS_ORG_UPDATE

# DHIS2 API credentials and URL



DHIS2_API_POST_URL =  "https://uin.ippf.org/api/"
DHIS2_AUTH_POST = ("*****", "******")

# Create a session object for persistent connection

#session_post = requests.Session()
#session_post.auth = DHIS2_AUTH_POST

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log filename
#log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = LOG_FILE_USERS_ORG_UPDATE
#log_filename = f"{LOG_FILE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)

#BASE_URL = "https://your-dhis2-url/api/"
#USERNAME = "****"
#PASSWORD = "****"

#session_post = requests.Session()
#session.auth = (USERNAME, PASSWORD)
#session_post.headers.update({"Content-Type": "application/json"})


session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST
session_post.headers.update({
    "Accept": "application/json",
    "Content-Type": "application/json"
})

import math

def clean_nan(obj):
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items() if not (isinstance(v, float) and math.isnan(v))}
    elif isinstance(obj, list):
        return [clean_nan(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj


current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"user TEI Search OrgUnit Updation start at. { current_time_start }" )
logging.info(f"user TEI Search OrgUnit Updation start at. { current_time_start }")

# -------------------------------
# Read Excel and convert to JSON
# -------------------------------

#df = pd.read_excel("usersPost_242_mynmar_demo_11March2026.xlsx", sheet_name="usersPost242")
df = pd.read_excel("user_tei_search_orgunits_update.xlsx", sheet_name="user_tei_search_orgunits_update")
# Convert NaN → None
df = df.where(pd.notnull(df), None)

records = df.to_dict(orient="records")

print(f"Total rows in Excel: {len(records)}")
logging.info(f"Total rows in Excel: {len(records)}")

success = 0
failed = 0
skipped = 0

# -------------------------------
# Process each record
# -------------------------------
for i, row in enumerate(records, start=1):


    username = row.get("username")

    # Check if user exists
    get_url = f"{DHIS2_API_POST_URL}users.json?filter=username:eq:{username}&fields=*&paging=false"
    #print(f"Row {i}: get_url → {get_url}")
    get_response = session_post.get(get_url)

    #data = get_response.json()

    try:
        data = get_response.json()
        #print(f"Row {i}: user_get_response → {data}")
    except ValueError:
        print("Invalid JSON response")
        print("Status:", get_response.status_code)
        #print("Response:", get_response.text)
        data = {"users": []}

    if len(data.get("users", [])) > 0:
        user = data["users"][0]

        user_id = user['id']
        user_name = user['username']

        print(f"Row {i}: Username exists name → {user_name}")
        logging.info(f"Row {i}: Username exists name : {user_name}")
        
        updateUserTeiSearchOrgUnit = user
    
        #This handles: None,NaN,empty string "", spaces " "
        '''
        if pd.notna(row.get("teiSearchOrganisationUnits")) and str(row.get("teiSearchOrganisationUnits")).strip():
            updateUserTeiSearchOrgUnit["teiSearchOrganisationUnits"] = [
            {"id": x.strip()}for x in str(row["teiSearchOrganisationUnits"]).split(",")if x.strip()
        ]
        '''

        #This handles: None,NaN,empty string "", spaces " "
        if pd.notna(row.get("organisationUnits")) and str(row.get("organisationUnits")).strip():
            updateUserTeiSearchOrgUnit["organisationUnits"] = [
            {"id": x.strip()}for x in str(row["organisationUnits"]).split(",")if x.strip()
        ]
        
        #This handles: None,NaN,empty string "", spaces " "
        if pd.notna(row.get("dataViewOrganisationUnits")) and str(row.get("dataViewOrganisationUnits")).strip():
            updateUserTeiSearchOrgUnit["dataViewOrganisationUnits"] = [
            {"id": x.strip()}for x in str(row["dataViewOrganisationUnits"]).split(",")if x.strip()
        ]

        #This handles: None,NaN,empty string "", spaces " "
        if pd.notna(row.get("teiSearchOrganisationUnits")) and str(row.get("teiSearchOrganisationUnits")).strip():
            updateUserTeiSearchOrgUnit["teiSearchOrganisationUnits"] = [
            {"id": x.strip()}for x in str(row["teiSearchOrganisationUnits"]).split(",")if x.strip()
        ]


        put_url = f"{DHIS2_API_POST_URL}users/{user_id}"

        put_response = session_post.put(
            put_url,
            json=updateUserTeiSearchOrgUnit
        )

        if put_response.status_code in [200, 201, 204]:
            print(f"Row {i}: User TEI Search OrgUnit Updated success → {put_response.json()}")
            logging.info(f"Row {i}: User TEI Search OrgUnit Updated success : {put_response.json()}")

            success += 1
        else:
            print(f"Row {i}: Failed → {put_response.text}")
            logging.error(f"Row {i}: Failed : {put_response.text}")
            failed += 1
    print("-" * 50)
    logging.info("-" * 50)

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
print( f"user TEI Search OrgUnit Updation end at. { current_time_end }" )
logging.info(f"user TEI Search OrgUnit Updation end at. { current_time_end }")