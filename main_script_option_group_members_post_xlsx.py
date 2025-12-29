#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
dhis2_username = "******"
dhis2_password = "******"

from constants import LOG_FILE_OPTION_GRP_MEMBERS_PUT, LOG_FILE_EVENT_ERROR_LOG

# DHIS2 API credentials and URL

DHIS2_API_GET_URL = "https://hmistraining.mm.dhis2.net/train/api/"
DHIS2_AUTH_GET = ("*****", "*****")

dhis2_username = "*****"
dhis2_password = "*****"

#DHIS2_API_POST_URL = "https://links.hispindia.org/nepal_climate/api/"
DHIS2_API_POST_URL =  "https://hmistraining.mm.dhis2.net/train/api/"

#DHIS2_AUTH_POST = ("*****", "*****")
DHIS2_AUTH_POST = ("*****", "******")

#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session_get = requests.Session()
session_get.auth = DHIS2_AUTH_GET

session_post = requests.Session()
session_post.auth = DHIS2_AUTH_POST

logging.basicConfig(filename=LOG_FILE_OPTION_GRP_MEMBERS_PUT, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"option Group members post start . { current_time_start }" )
logging.info(f"option Group members post start . { current_time_start }")

tei_data_cache = {}
events_by_reg_id = {}

def assign_value_if_not_null(value):
    if value is not None and value != "null":
        return value
    elif value.isna():
            return ""
    else:
        return ""

def assign_value_if_NaN(value):
    if pd.notnull(value):
        return value
    else:
        return ""

def get_option_group_details(session_post,option_grp_uid):
    
    option_grp_get_url = f"{DHIS2_API_GET_URL}optionGroups/{option_grp_uid}.json"

    #print(option_grp_get_url)
    #print(f" event_search_url : {event_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session_get.get(option_grp_get_url)
    
    if response.status_code == 200:
        option_grp_response_data = response.json()
        #print(response)
        #print(option_grp_response_data)
        return option_grp_response_data 
    else:
        return []
    
def push_option_grp_member_in_dhis2(session_post, option_group_response_data, option_group_uid, option_group_name ):
    #
    try:
        option_grp_member_put_url = f"{DHIS2_API_POST_URL}optionGroups/{option_group_uid}"
        #event_update_url = f"{dhis2_api_url}events/{eventUID}/{dataElementUid}"
        response = session_post.put(option_grp_member_put_url, data=json.dumps(option_group_response_data), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        #global  option_grp_sl_no
        #option_grp_sl_no = option_grp_sl_no + 1
        print(f"Option Group Member created successfully option_group_uid, : {option_group_uid}, and option_group_name: {option_group_name}")
        logging.info(f"Option Group Member created successfully option_group_uid, : {option_group_uid}, and option_group_name: {option_group_name}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        
        print(f"Failed to create Option. for option_group_uid, : {option_group_uid}, and option_group_name: {option_group_name}, resp_msg: {resp_msg} ")
        logging.error(f"Failed to create Option for option_group_uid, : {option_group_uid}, and option_group_name: {option_group_name}, resp_msg: {resp_msg}")


#event_to_event_post_excel_file_path = 'timor_event_to_event_post.xlsx'
#option_grp_member_post_excel_file_path = 'Option_Group_members_Import_Village.xlsx'
option_grp_member_post_excel_file_path = 'Option_Group_members_Import_Ward.xlsx'


print( f"file_name . { option_grp_member_post_excel_file_path }" )
logging.info(f"file_name . { option_grp_member_post_excel_file_path }")


with ThreadPoolExecutor(max_workers=1) as executor:
    # Create a session object for persistent connection
    # add dtype='object' for ready text start from 0
    # Load Excel
    
    #event_push_count = 0

    option_grp_member_list = pd.read_excel(option_grp_member_post_excel_file_path, dtype='object')

    print( f"length of option_grp_member_list. { len(option_grp_member_list) }" )
    logging.info( f"length of option_grp_member_list . { len(option_grp_member_list) }" )


    # Group by Option Group Name/ Option Group UID
    for group_uid, group_df in option_grp_member_list.groupby("Option Group UID"):
        
        # Option Set UID (same for the group)
        option_set_uid = group_df["Option Set UID"].iloc[0]
        option_group_uid = group_df["Option Group UID"].iloc[0]
        option_group_name = group_df["Option Group Name"].iloc[0]

        print( f"option_group_uid . { option_group_uid }" )

        option_group_response_data = get_option_group_details( session_post, option_group_uid )

        # Build options list
        options_list = []
        for _, row in group_df.iterrows():
            options_list.append({
                "id": row["option UID"]
            })

        if option_group_response_data:
            
            option_group_response_data["options"] = options_list

            #print( f"option_group_response_data_payload . { option_group_response_data }" )
            #logging.info(f"event_payload . { option_group_response_data }")
            #executor.submit( push_events_in_dhis2, session, event_payload, eventUid, index+1 )
            executor.submit( push_option_grp_member_in_dhis2, session_post, option_group_response_data, option_group_uid, option_group_name )

        '''
        # Build options list
        options_list = []
        for _, row in group_df.iterrows():
            options_list.append({
                "id": row["option UID"],
                "code": row["Code"],
                "name": row["Shortname"]
            })

        print( f"options_list . { options_list }" )

        # Final JSON structure
        option_set_json = {
            "id": option_set_uid,
            "name": group_name,
            "options": options_list
        }

        # Save JSON
        file_path = os.path.join(output_dir, f"{safe_group_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(option_set_json, f, indent=2, ensure_ascii=False)

        print(f"Created: {file_path}")

        '''

 
current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"option Group members post end . { current_time_end }" )
logging.info(f"option Group members post end . { current_time_end }")

