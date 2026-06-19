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

from constants import LOG_FILE_USERS_POST

# DHIS2 API credentials and URL

#DHIS2_API_GET_URL = "https://hmistraining.mm.dhis2.net/train/api/"
#DHIS2_AUTH_GET = ("******", "*******")



DHIS2_API_POST_URL =  "https://uin.ippf.org/api/"
DHIS2_AUTH_POST = ("*******", "*******")


# Create a session object for persistent connection

#session_post = requests.Session()
#session_post.auth = DHIS2_AUTH_POST

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log filename
#log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = LOG_FILE_USERS_POST
#log_filename = f"{LOG_FILE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)

#BASE_URL = "https://your-dhis2-url/api/"
#USERNAME = "admin"
#PASSWORD = "district"

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
print( f"user creation start at. { current_time_start }" )
logging.info(f"user creation start at. { current_time_start }")

# -------------------------------
# Read Excel and convert to JSON
# -------------------------------

#df = pd.read_excel("usersPost_242_mynmar_demo_11March2026.xlsx", sheet_name="usersPost242")
df = pd.read_excel("usersPost_242.xlsx", sheet_name="usersPost242")
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
    get_url = f"{DHIS2_API_POST_URL}users.json?filter=username:eq:{username}&fields=id,name,username&paging=false"
    #print(f"Row {i}: get_url → {get_url}")
    get_response = session_post.get(get_url)

    #data = get_response.json()

    try:
        data = get_response.json()
        print(f"Row {i}: user_get_response → {data}")
    except ValueError:
        print("Invalid JSON response")
        print("Status:", get_response.status_code)
        #print("Response:", get_response.text)
        data = {"users": []}

    if len(data.get("users", [])) > 0:
        user = data["users"][0]
        print(f"Row {i}: Username already exists name → {user['username']}")
        logging.info(f"Row {i}: Username already exists name : {user['username']}")
        skipped += 1
        continue

    
    usersPost = {
        "id": row.get("userInfoUid"),
        "firstName": row.get("firstName"),
        "surname": row.get("surname"),
        "email": row.get("email"),
        "phoneNumber": row.get("phoneNumber"),
        "username": row.get("username"),
        "password": row.get("password"),
    }

    # Organisation Units
    if row.get("organisationUnits"):
        usersPost["organisationUnits"] = [{"id": row["organisationUnits"]}]

    if row.get("dataViewOrganisationUnits"):
        usersPost["dataViewOrganisationUnits"] = [{"id": row["dataViewOrganisationUnits"]}]

    if row.get("teiSearchOrganisationUnits"):
        usersPost["teiSearchOrganisationUnits"] = [{"id": row["teiSearchOrganisationUnits"]}]
    
    '''
    if row.get("userGroups"):
        usersPost["userGroups"] = [{"id": x.strip()} for x in str(row["userGroups"]).split(",")]
    
    '''
    #strip() removes spaces (and other whitespace characters like tabs/newlines) from the beginning and end of a string.
    '''
    text = "   abc123   "
    print(text.strip()) -- abc123
    '''
    
    #This handles: None,NaN,empty string "", spaces " "
    if pd.notna(row.get("userGroups")) and str(row.get("userGroups")).strip():
        usersPost["userGroups"] = [
            {"id": x.strip()}for x in str(row["userGroups"]).split(",")if x.strip()
        ]

    '''
    if row.get("userRoles"):
        usersPost["userRoles"] = [{"id": x.strip()} for x in str(row["userRoles"]).split(",")]
    '''
    
    #This handles: None,NaN,empty string "", spaces " "
    if pd.notna(row.get("userRoles")) and str(row.get("userRoles")).strip():
        usersPost["userRoles"] = [
            {"id": x.strip()} for x in str(row["userRoles"]).split(",") if x.strip()
        ]        

    # POST user
    # remove None values
    
    #usersPost = {k: v for k, v in usersPost.items() if v is not None}
    #post_response = session_post.post(DHIS2_API_POST_URL + "users", json=usersPost)

    usersPost = clean_nan(usersPost)
    #print("user_post_Payload:", usersPost)   # optional debug

    post_response = session_post.post(
        DHIS2_API_POST_URL + "users",
        json=usersPost
    )

    if post_response.status_code in [200, 201]:
        #print(f"Row {i}: User Created")
        print(f"Row {i}: User Created success → {post_response.json()}")
        logging.info(f"Row {i}: User Created success : {post_response.json()}")

        success += 1
    else:
        print(f"Row {i}: Failed → {post_response.text}")
        logging.error(f"Row {i}: Failed : {post_response.text}")
        failed += 1


# -------------------------------
# DHIS2 Import Summary
# -------------------------------
print("\n========== DHIS2 IMPORT SUMMARY ==========")
logging.info(f"\n========== DHIS2 IMPORT SUMMARY ==========")
print(f"Total Records : {len(records)}")
logging.info(f"Total Records : {len(records)}")
print(f"Created       : {success}")
logging.info(f"Created       : {success}")
print(f"Skipped       : {skipped}")
logging.info(f"Skipped       : {skipped}")
print(f"Failed        : {failed}")
logging.info(f"Failed        : {failed}")
print("==========================================")
logging.info("==========================================")

current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"user creation end at. { current_time_end }" )
logging.info(f"user creation end at. { current_time_end }")