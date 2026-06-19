#import mysql_connection
#import dhis2_integration
from concurrent.futures import ThreadPoolExecutor
#from dhis2_api_interaction import get_orgunit_grp_member
import requests
import json
import logging, datetime
import pandas as pd
from requests.auth import HTTPBasicAuth

import urllib3 ## for disable warning of Certificate
urllib3.disable_warnings() ## for disable warning of Certificate



from constants import LOG_FILE_TEI_TETYPE_VALUE_UPDATE, LOG_FILE_TEI_TETYPE_VALUE_ERROR_LOG

# DHIS2 API credentials and URL


# DHIS2 API credentials and URL

#DHIS2_API_URL = "https://hmis.moh.gov.mm/events/api/"
#DHIS2_API_URL = "https://links.hispindia.org/ippf_uin/api/"
DHIS2_API_URL = "https://hmistraining.mm.dhis2.net/train/api/"
DHIS2_AUTH = ("******", "******")


#https://tracker.hivaids.gov.np/save-child-2.27/api/sqlViews/P8cFNnfn9UP/data?paging=false

# Create a session object for persistent connection
session = requests.Session()
session.auth = DHIS2_AUTH

logging.basicConfig(filename=LOG_FILE_TEI_TETYPE_VALUE_UPDATE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#with requests.Session() as session:
    #session.auth = (un, pw)


# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"update TEI trackedentitytype start . { current_time_start }" )
logging.info(f"update TEI trackedentitytype start . { current_time_start }")


def get_sqlview_data(session):
    
    # event_list_for_migration = sw9NLEwlWXp , iltiuz4RgKs
   
    sql_view_url = f"{DHIS2_API_URL}sqlViews/sw9NLEwlWXp/data.json?paging=false"

    print(f"sql_view_url : {sql_view_url}")

    #response_sql_view = requests.get(sql_view_url,auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    
    response_sql_view = session.get(sql_view_url, verify=False)
    
    #print(f"response_sql_view : {response_sql_view.text}")

    if response_sql_view.status_code == 200:
        #print(f"response_sql_view : {response_sql_view.status_code}")
        response_sql_view_data = response_sql_view.json()
        #print(f"response_sql_view_data : {response_sql_view_data}")
        tempListGrid   = response_sql_view.json().get('listGrid', {})
        #print(f"tempListGrid : {tempListGrid}")
        #print(f"title : {tempListGrid.get('title')}")
        tempRows = tempListGrid.get('rows',[])

        if tempRows:
            for rows in tempRows:
                event = rows[0]
                orgUnit = rows[1]
                #print(f"event : {event}, org : {orgUnit}")
                
        else:
            error_message = f"No data received for sqlview"
            print(error_message)

        #print(tempRows)

    else:
        print(f"Failed to retrieve sqlview data. Status code: {response_sql_view.status_code}")

    return tempRows

# just make everything to string
def to_String(val):
    if val=='' or pd.isna(val):
        return ''
    else:
        return str(val)

def int_to_float(val):
    if val=='' or pd.isna(val):
        return ''
    else:
        return float(val)


def get_tei_details(session, tei_uid, program_uid):
    
    #https://ln4.hispindia.org/timor_dev/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
   
    
    #event_search_url = f"{event_push_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={programID}&status=ACTIVE&skipPaging=true&filter={event_search_dataElement_uid}:eq:{BenCallID}"
    tei_get_url = f"{DHIS2_API_URL}trackedEntityInstances/{tei_uid}.json?program={program_uid}"

    #print(tei_get_url)
    #print(f" event_search_url : {event_get_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session.get(tei_get_url)
    
    if response.status_code == 200:
        tei_response_data = response.json()
        #print(response)
        #print(tei_response_data)
       
        #print(f"tei_response_data trackedEntityInstance : {tei_response_data.get('trackedEntityInstance')}" )
        teiattributesValue = tei_response_data.get('attributes',[])
       
        #print(f"teiattributesValue : {teiattributesValue}" )
        return tei_response_data 
    else:
        return []

def update_tei_trackedentitytype_in_dhis2(session, update_tei_trackedentitytype, tei_uid, row_no ):
    #
    try:
        tei_trackedentitytype_update_url = f"{DHIS2_API_URL}trackedEntityInstances/{tei_uid}"

        #event_update_url = f"{dhis2_api_url}events/{eventUID}/{dataElementUid}"
        response = session.put(tei_trackedentitytype_update_url, data=json.dumps(update_tei_trackedentitytype), headers={"Content-Type": "application/json"}, verify=False)
        response.raise_for_status()

        if response.status_code == 200:
            conflictsDetails   = response.json().get("response", {}).get("conflicts")
       
            print(f"TEI updated successfully. Row No : {row_no}. updated tei : {tei_uid}.")
            logging.info(f"TEI updated successfully. Row No : {row_no}. updated tei : {tei_uid}.")
            #logging.info(f"Event created successfully . BenVisitID : {BenVisitID} . BeneficiaryRegID : {BeneficiaryRegID}. Event count: {event_count}. Event uid: {event_uid}" )
            #logging.info("MySQL connection closed")

        else:
            print(f"Failed to update TEI trackedentitytype. Error: {response.text}")
            logging.error(f"Failed to update TEI trackedentitytype. Row No : {row_no} .conflictsDetails : {conflictsDetails} .Status code: {response.status_code} .error details: {response.json()} .Error: {response.text}")

    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        #print(f'####################################################### FAILED #######################################################', flush=True)
        #print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
        #print(f"Failed to create events. Error: {response.text}")
        #logging.error(f"Failed to create events .event_uid : {event_uid} . row : {row} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

        with open(LOG_FILE_TEI_TETYPE_VALUE_ERROR_LOG, 'a') as fail_record:
            fail_record.write(f'\ncurrent tei_uid: {tei_uid}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f" Failed to update TEI trackedentitytype. Error: {response.text}")
        logging.error(f"Failed to update TEI trackedentitytype . tei_uid : {tei_uid} . row : {row_no} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


tei_trackedentityType_update_excel_file_path = 'updateTeiTrackedentityType.xlsx'
print( f"file_name . { tei_trackedentityType_update_excel_file_path }" )
logging.info(f"file_name . { tei_trackedentityType_update_excel_file_path }")

with ThreadPoolExecutor(max_workers=10) as executor:
    # Create a session object for persistent connection
    
    tei_list = pd.read_excel(tei_trackedentityType_update_excel_file_path)
    #print( f"length of tei. { tei_list }" )
    print( f"length of tei. { len(tei_list) }" )
    logging.info( f"length of tei . { len(tei_list) }" )
    #for index, eventDataValueRow in updateEventDataValues.iterrows():
    
    for index, teiRow in tei_list.iterrows():
        #print( f"teiRow. {teiRow} " )
        #print( f"teiRow. {teiRow['tei']} {teiRow['program']}, {str(teiRow['attributeValue'])} " )
        tei_response_data = get_tei_details( session, teiRow['tei'], teiRow['program']  )

        if tei_response_data:
            
            #update_tei_trackedentitytype = tei_response_data

            existing_attributes = tei_response_data.get("attributes", [])
            update_tei_trackedentitytype_payload = {
                "orgUnit": tei_response_data.get('orgUnit'),
                "attributes": existing_attributes,
                "trackedEntityType":teiRow.get("trackedEntityType")
            }
            
            print( f"update_tei_trackedentitytype . { update_tei_trackedentitytype_payload }" )
            #logging.info(f"event_payload . { event_payload }")
            executor.submit( update_tei_trackedentitytype_in_dhis2, session, update_tei_trackedentitytype_payload, teiRow['tei'], index+1 )
        

current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f"update TEI trackedentitytype end . { current_time_end }" )
logging.info(f"update TEI trackedentitytype end . { current_time_end }")

