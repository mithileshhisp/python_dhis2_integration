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

from constants import LOG_FILE_USERS_UPDATE

# DHIS2 API credentials and URL

#DHIS2_API_GET_URL = "****/api/"
#DHIS2_AUTH_GET = ("*****", "*****")


#DHIS2_API_POST_URL = "******/api/"
#DHIS2_API_POST_URL =  "******/api/"
#DHIS2_AUTH_POST = ("*****", "*****")

DHIS2_API_POST_URL =  "******/api/"
DHIS2_AUTH_POST = ("*****", "*****")

# Create a session object for persistent connection

#session_post = requests.Session()
#session_post.auth = DHIS2_AUTH_POST

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create unique log filename
#log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = LOG_FILE_USERS_UPDATE
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
print( f"user Updation start at. { current_time_start }" )
logging.info(f"user Updation start at. { current_time_start }")

# -------------------------------
# Read Excel and convert to JSON
# -------------------------------
df = pd.read_excel("userPasswordUpdate.xlsx", sheet_name="userPasswordUpdate")
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

    username = row["username"]
    password = row["password"]

    # Check if user exists
    #get_url = f"{DHIS2_API_POST_URL}users.json?filter=username:eq:{username}&fields=id,name,username&paging=false"
    
    # STEP 1: FIND USER BY USERNAME
    search_url = f"{DHIS2_API_POST_URL}users.json"
    params = {
            "filter": f"userCredentials.username:eq:{username}",
            "fields": "id,name",
            "paging": "false"
    }
    
    
    #print(f"Row {i}: get_url → {get_url}")
    #get_response = session_post.get(get_url)

    response = session_post.get(search_url, params=params)
    response.raise_for_status()
    userResponse = response.json()

    users = userResponse.get("users", [])

    if len(users) != 0:
        user_id = users[0]["id"]
        user_name = users[0]["name"]

        print(f"Username taken with user id {user_id} and name {user_name}")
        logging.info(f"Row {i}: Username taken with user id {user_id} and name {user_name}")

        # STEP 2: GET FULL USER OBJECT
        get_user_url = f"{DHIS2_API_POST_URL}users/{user_id}.json?paging=false"
        tempUserResponse = session_post.get(get_user_url)
        tempUserResponse.raise_for_status()

        updateUserPassword = tempUserResponse.json()

        # UPDATE PASSWORD
        updateUserPassword["userCredentials"]["password"] = password

        # STEP 3: PUT UPDATE
        put_url = f"{DHIS2_API_POST_URL}users/{user_id}"

        put_response = session_post.put(
            put_url,
            data=json.dumps(updateUserPassword)
        )

        if put_response.status_code in [200, 201]:
            #print(f"Row - {import_count} update done response: {put_response.text}")
            #print(f"Row {i}: User Created")
            print(f"Row {i}: User Update success → {user_name}")
            logging.info(f"Row {i}: User Update success : {put_response.json()}")

            success += 1
        else:
            #print(f"Row - {import_count} error response: {put_response.text}")
            print(f"Row {i}: Failed → {put_response.text}")
            logging.error(f"Row {i}: Failed : {put_response.text}")
            failed += 1

    else:
        print("Username not present")
        logging.info(f"Row {i}: Username not present : {user_name}")



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
print( f"user Updation end at. { current_time_end }" )
logging.info(f"user Updation end at. { current_time_end }")




'''
import pandas as pd
import requests
import json

# CONFIGURATION
DHIS2_BASE_URL = "https://your-dhis2-url/api/"
USERNAME = "your_username"
PASSWORD = "your_password"

session = requests.Session()
session.auth = (USERNAME, PASSWORD)
session.headers.update({"Content-Type": "application/json"})

# READ EXCEL
file_path = "input.xlsx"
sheet_name = "userPasswordUpdate"

df = pd.read_excel(file_path, sheet_name=sheet_name)

import_count = 1

for index, row in df.iterrows():
    import_count += 1
    username = row["username"]
    password = row["password"]

    try:
        # STEP 1: FIND USER BY USERNAME
        search_url = f"{DHIS2_BASE_URL}users.json"
        params = {
            "filter": f"userCredentials.username:eq:{username}",
            "fields": "id,name",
            "paging": "false"
        }

        response = session.get(search_url, params=params)
        response.raise_for_status()
        userResponse = response.json()

        users = userResponse.get("users", [])

        if len(users) != 0:
            user_id = users[0]["id"]
            name = users[0]["name"]

            print(f"Username taken with user id {user_id} and name {name}")

            # STEP 2: GET FULL USER OBJECT
            get_user_url = f"{DHIS2_BASE_URL}users/{user_id}.json?paging=false"
            tempUserResponse = session.get(get_user_url)
            tempUserResponse.raise_for_status()

            updateUserPassword = tempUserResponse.json()

            # UPDATE PASSWORD
            updateUserPassword["userCredentials"]["password"] = password

            # STEP 3: PUT UPDATE
            put_url = f"{DHIS2_BASE_URL}users/{user_id}"

            put_response = session.put(
                put_url,
                data=json.dumps(updateUserPassword)
            )

            if put_response.status_code in [200, 201]:
                print(f"Row - {import_count} update done response: {put_response.text}")
            else:
                print(f"Row - {import_count} error response: {put_response.text}")

        else:
            print("Username not present")

    except Exception as e:
        print(f"{username} -- Error!: {str(e)}")

if import_count == len(df) + 1:
    print("update done")
'''    