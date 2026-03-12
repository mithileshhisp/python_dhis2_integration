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

import math

from constants import LOG_FILE_USERS_DELETE


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log filename
#log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = LOG_FILE_USERS_DELETE
#log_filename = f"{LOG_FILE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)

#BASE_URL = "https://your-dhis2-url/api/"
#USERNAME = "*****"
#PASSWORD = "*****"

#session_post = requests.Session()
#session.auth = (USERNAME, PASSWORD)
#session_post.headers.update({"Content-Type": "application/json"})

# DHIS2 config

# DHIS2 API credentials and URL
# Create a session object for persistent connection
#session_post = requests.Session()
#session_post.auth = DHIS2_AUTH_POST

DHIS2_API_POST_URL =  "*****/api/"
DHIS2_AUTH_POST = ("******", "******")
session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST
session_post.headers.update({
    "Accept": "application/json",
    "Content-Type": "application/json"
})


def clean_nan(obj):
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items() if not (isinstance(v, float) and math.isnan(v))}
    elif isinstance(obj, list):
        return [clean_nan(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj


current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"user deletion start at. { current_time_start }" )
logging.info(f"user deletion start at. { current_time_start }")

# Read Excel
# -------------------------------
# Read Excel and convert to JSON
# -------------------------------
df = pd.read_excel("usersDelete_242_mynmar_demo_11March2026.xlsx", sheet_name="usersDelete242")

print("Total rows in Excel:", len(df))

deleted = 0
not_found = 0
failed = 0

for i, row in df.iterrows():

    username = str(row["username"]).strip()

    # Step 1: Find user by username
    get_url = f"{DHIS2_API_POST_URL}users.json?filter=username:eq:{username}&fields=id,name,username&paging=false"

    response = session_post.get(get_url)
    data = response.json()

    if len(data.get("users", [])) == 0:
        print(f"Row {i+1}: User not found user name → {username}")
        logging.info(f"Row {i+1}: User not found user name : {username}")
        not_found += 1
        continue

    user_id = data["users"][0]["id"]

    print(f"Row {i+1}: Found user name {username} user id → {user_id}")
    logging.info(f"Row {i+1}: Found user name {username} user id : {user_id}")

    # Step 2: Delete user
    delete_url = f"{DHIS2_API_POST_URL}users/{user_id}"
    delete_response = session_post.delete(delete_url)

    if delete_response.status_code in [200, 204]:
        print(f"Row {i+1}: Deleted → {username}")
        logging.info(f"Row {i+1}: Deleted user name {username} user id : {user_id}")
        deleted += 1
    else:
        print(f"Row {i+1}: Failed → {delete_response.text}")
        logging.error(f"Row {i+1}: Failed to Deleted user name {username} user id : {user_id} with error, {delete_response.text}")
        failed += 1


print("\n========== DELETE SUMMARY ==========")
logging.info(f"\n========== DELETE SUMMARY ==========")
print("Total Excel Users:", len(df))
logging.info(f"Total Excel Users:, {len(df)}")
print("Deleted:", deleted)
logging.info(f"Deleted:, {deleted}")
print("Not Found:", not_found)
logging.info(f"Not Found:, {not_found}")
print("Failed:", failed)
logging.info(f"Failed:, {failed}")

current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"user deletion end at. { current_time_end }" )
logging.info(f"user deletion end at. { current_time_end }")