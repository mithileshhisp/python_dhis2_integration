#import mysql_connection
#import dhis2_integration
import requests
import json
from dhis2_api_interaction import assign_value_if_not_null,format_date
import database_connection
import logging, datetime
import pandas as pd
from database_connection import connect_to_mysql
from constants import LOG_FILE_WISEPILL_EVENT, LOG_FILE_WISEPILL_EVENT_ERROR_LOG
# DHIS2 API credentials and URL
DHIS2_API_URL = "/api/"
DHIS2_AUTH = ("*****", "******")
enrollment_endpoint = f"{DHIS2_API_URL}trackedEntityInstances"
event_endpoint = f"{DHIS2_API_URL}events"

program_uid="RUqNUsv6WBp"
program_stage = "cSHkx58Kma3"
device_IMEI_attr_uid = "D7chPF3UUUy" 
event_search_dataElement_uid = "alV2b3AtVLw"

# Create a session object for persistent connection
session = requests.Session()
session.auth = DHIS2_AUTH

evrimed_wisepill_get_url = "/api/v1/"
evrimed_wisepill_username = "*******"
evrimed_wisepill_secert = "*******"

logging.basicConfig(filename=LOG_FILE_WISEPILL_EVENT, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get the current date and time
current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" getting evrimed_wisepill_episodes start . { current_time_start }" )
logging.info(f" getting evrimed_wisepill_episodes start . { current_time_start }")


# The DHIS2 API endpoint
program_stage_url = f"{DHIS2_API_URL}programStages/{program_stage}?fields=programStageDataElements[id,name,dataElement[id,name,code]]"

# Make the GET request with the session
response = session.get(program_stage_url)
# Error handling for JSON response
if response.status_code == 200:
    try:
        program_stage_data = response.json()  # Try parsing the response as JSON
    except ValueError:
        logging.error("Error: Failed to decode JSON. Check the API response content.")
        logging.error(response.text)
        exit()
else:
    logging.error(f"Error: API request failed with status code {response.status_code}")
    logging.error(response.text)
    exit()

# Step 5: Map the data elements by their code, and handle 'calculate_drugs' elements specially
data_element_mapping = {
    element['dataElement']['code']: element['dataElement']['id']
    for element in program_stage_data['programStageDataElements']
}

#data_element_id = data_element_mapping['episode_id']
#print(f"data_element_id {data_element_id}")

#evrimed_wisepill_episodes = get_evrimed_wisepill_episodes()
#print(f"evrimed_wisepill_episodes size {len(evrimed_wisepill_episodes)}")

def get_sqlview_data_device_imei():
    
    # age_on_visit = P8cFNnfn9UP
    # sex = wGdLwfDzjyG
    # FSW type = GWdWZBnvv0G
    # Client of FSW type = CTAfO6mvhTl
    # Risk group = nQT7OA90MOq
    # Marital status = qYJQyXbZesE
    sql_view_url = f"{DHIS2_API_URL}sqlViews/YoENx5aVL24/data?paging=false"

    #print(f"sql_view_url : {sql_view_url}")

    #response_sql_view = requests.get(sql_view_url,auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    
    response_sql_view = session.get(sql_view_url)
    
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
                device_imei = rows[0]
                #dataValue = rows[1]
                print(f"device_imei : {device_imei}")
                
        else:
            error_message = f"No data received for sqlview"
            print(error_message)

        #print(tempRows)

    else:
        print(f"Failed to retrieve sqlview data. Status code: {response_sql_view.status_code}")

    return tempRows


def get_evrimed_wisepill_episodes( device_imei ):
    
    response_data_episodes_records = []
    #header = {"Authorization" : "Username" : {evrimed_wisepill_username}, "Secret" : {evrimed_wisepill_username}}


    #headers = {"content-type": "application/json; charset=UTF-8",'Authorization':'Bearer {}'.format(access_token)}

    #headers = {"content-type": "application/json", "Username" : {evrimed_wisepill_username}, "Secret" : {evrimed_wisepill_username}}

    evrimed_wisepill_episodes = list()
    #https://evrimed.wisepill.com/sbapi/v1/episodes/getEpisodes?device_imei=865340054256718&calendar=1
    #https://ln4.hispindia.org/timor_dev/api/programIndicatorGroups/IbAL4Ou7Rfl.json?fields=id,name,programIndicators[id,name]&paging=false
    url_get_episodes = f"{evrimed_wisepill_get_url}episodes/getEpisodes?device_imei={device_imei}&calendar=1"

    #print(f"url_get_episodes : {url_get_episodes}")

    headers = {
        'Username': 'who_timor-leste',
        'Secret': '312aaabb736dcec183a58cda9dcd4a23'
    }

    response_evrimed_wisepill_episodes = requests.get(url_get_episodes, headers=headers)

    #print(f"response_evrimed_wisepill_episodes : {response_evrimed_wisepill_episodes.status_code}")
    
    if response_evrimed_wisepill_episodes.status_code == 200:

        response_data_episodes = response_evrimed_wisepill_episodes.json()
        #print(f"response_data_episodes : {response_data_episodes.get('Result')}")
        if response_data_episodes.get('Result') != 'Episode not found':
        
            response_data_episodes_records = response_data_episodes.get('records', [])
            #print(f"response_data_episodes_records : {response_data_episodes_records}")
            if response_data_episodes_records:
            
                response_data_episodes_records = response_data_episodes_records
            #for episode_details in response_data_episodes_records:
                
                #if episode_details:
                    #episode_id = assign_value_if_not_null(episode_details['episode_id'])
                    #device_imei = assign_value_if_not_null(episode_details['device_imei'])
                    #episode_start_date = assign_value_if_not_null(episode_details['episode_start_date'])
                    #print(f"episode_details. episode_id : {episode_id} . device_imei : {device_imei} . episode_start_date : {episode_start_date}")
                    
                                       
            #print(f"episodes_records_list size {len(response_data_episodes_records)}")
            print(f"Episode detail retrieved with device_imei : {device_imei}, {response_data_episodes.get('Result')}")
            logging.info(f"Episode detail retrieved with device_imei: {device_imei}, {response_data_episodes.get('Result')}" )

        else:
            print(f"Failed to retrieve evrimed_wisepill Episode not found with device_imei : {device_imei}, {response_data_episodes.get('Result')}")
            logging.info(f"Failed to retrieve evrimed_wisepill Episode not found with device_imei: {device_imei} {response_data_episodes.get('Result')}" )

    else:
         print(f"Failed to retrieve evrimed_wisepill Episode not found with device_imei : {device_imei},{response_data_episodes.get('Result')} ")
         logging.info(f"Failed to retrieve evrimed_wisepill Episode not found with device_imei: {response_evrimed_wisepill_episodes.status_code} {response_data_episodes.get('Result')}" )

    return response_data_episodes_records


def check_existing_tei(device_IMEI_no):
    
    #https://links.hispindia.org/amrit/api/trackedEntityInstances.json?ouMode=ALL&program=vyQPQ07JB9M&filter=HKw3ToP2354:eq:7393430
    #https://links.hispindia.org/timor/api/trackedEntityInstances.json?ouMode=ALL&program=RUqNUsv6WBp&filter=D7chPF3UUUy:eq:865340054256718
    #tei_search_url = f"{enrollment_endpoint}?ouMode=ALL&program=vyQPQ07JB9M&filter=HKw3ToP2354:eq:{beneficiary_mapping_reg_id}"
    tei_search_url = f"{enrollment_endpoint}?ouMode=ALL&program={program_uid}&filter={device_IMEI_attr_uid}:eq:{device_IMEI_no}"
    #print(tei_search_url)
    #response = requests.get(tei_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session.get(tei_search_url)
    if response.status_code == 200:
        response_data = response.json()
        teis = response_data.get('trackedEntityInstances', [])
        #print(f"TEI not found with device_imei no  {teis}")
        return teis 
    else:
        return []

def check_existing_event(orgUnitID,episode_id_de_uid, episode_id):
    
    #https://ln4.hispindia.org/timor_dev/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
   
    #https://links.hispindia.org/timor/api/events.json?orgUnit=Fn51zf6ifbm&ouMode=SELECTED&program=RUqNUsv6WBp&status=ACTIVE&skipPaging=true&filter=alV2b3AtVLw:eq:897
    #event_search_url = f"{event_push_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={programID}&status=ACTIVE&skipPaging=true&filter={event_search_dataElement_uid}:eq:{BenCallID}"
    event_search_url = f"{event_endpoint}?orgUnit={orgUnitID}&ouMode=SELECTED&program={program_uid}&status=ACTIVE&skipPaging=true&filter={episode_id_de_uid}:eq:{episode_id}"

    #print(event_search_url)
    #print(f" event_search_url : {event_search_url}" )
    #response = requests.get(event_search_url, auth=HTTPBasicAuth(dhis2_username, dhis2_password))
    response = session.get(event_search_url)
    if response.status_code == 200:
        response_data = response.json()
        events = response_data.get('events', [])
        return events 
    else:
        return []

def add_update_event(evrimed_wisepill_episodes):
    #print(f"evrimed_wisepill_episodes size 2 {len(evrimed_wisepill_episodes)}")
    for episode_details in evrimed_wisepill_episodes:
                    
        if episode_details:
            device_imei = assign_value_if_not_null(episode_details['device_imei'])
            episode_id = assign_value_if_not_null(episode_details['episode_id'])
            episode_start_date = assign_value_if_not_null(episode_details['episode_start_date'])
            adherence_string = assign_value_if_not_null(episode_details['adherence_string'])
            Calendar = assign_value_if_not_null(episode_details['Calendar'])
            last_seen = assign_value_if_not_null(episode_details['last_seen'])
            existing_tei = check_existing_tei(device_imei)
            #print(f"TEI not found with device_imei no  {existing_tei}")
            
            #print(f"episode_details. episode_id 1 : {episode_id} . device_imei : {device_imei} . episode_start_date : {episode_start_date}")
            #print(f"episode_details. adherence_string 2 : {adherence_string} . Calendar : {Calendar} . last_seen : {last_seen}")
            
            #orgUnit = existing_tei[0]['orgUnit']
            #tei_uid = existing_tei[0]['trackedEntityInstance']

            #print(f"TEI not found with device_imei no  {existing_tei}")
            #print(f"TEI not found with device_imei no  {tei_uid}")

            if not existing_tei:
                print(f"TEI not found with device_imei no  {device_imei}")
                logging.info(f"TEI not found with device_imei no  {device_imei}")
                return

            orgUnit = existing_tei[0]["orgUnit"]
            tei_uid = existing_tei[0]["trackedEntityInstance"]
            episode_id_de_uid = data_element_mapping['episode_id']
            existing_event = check_existing_event(orgUnit, episode_id_de_uid, episode_id)
            #print(f"TEI not found with device_imei no  {existing_event}")
            if existing_event:
                print(f"Event already exists for EventId {existing_event[0]['event']}. episode_id {episode_id}")
                logging.info(f"Event already exists for EventId {existing_event[0]['event']}. episode_id {episode_id}")
                
                event_payload = {
                    "event" : existing_event[0]['event'],
                    "program": program_uid,
                    "dataValues": [
                        {"dataElement": data_element_mapping['episode_id'], "value": assign_value_if_not_null(episode_details['episode_id'])},
                        {"dataElement": data_element_mapping['episode_status'], "value": assign_value_if_not_null(episode_details['episode_status'])},
                        {"dataElement": data_element_mapping['last_battery_level'], "value": assign_value_if_not_null(episode_details['last_battery_level'])},
                        {"dataElement": data_element_mapping['total_device_days'], "value": assign_value_if_not_null(episode_details['total_device_days'])},
                        {"dataElement": data_element_mapping['total_device_dose_days'], "value": assign_value_if_not_null(episode_details['total_device_dose_days'])},
                        {"dataElement": data_element_mapping['total_episode_days'], "value": assign_value_if_not_null(episode_details['total_episode_days'])},
                        {"dataElement": data_element_mapping['Calendar'], "value": assign_value_if_not_null(episode_details['Calendar'])},
                        {"dataElement": data_element_mapping['episode_end_date'], "value": assign_value_if_not_null(episode_details['episode_end_date'])},
                        {"dataElement": data_element_mapping['episode_start_date'], "value": assign_value_if_not_null(episode_details['episode_start_date'])},
                        {"dataElement": data_element_mapping['last_seen'], "value": assign_value_if_not_null(episode_details['last_seen'])},
                        {"dataElement": data_element_mapping['last_signal_strength'], "value": assign_value_if_not_null(episode_details['last_signal_strength'])},
                        {"dataElement": data_element_mapping['last_opened'], "value": assign_value_if_not_null(episode_details['last_opened'])},
                        {"dataElement": data_element_mapping['episode_status'], "value": assign_value_if_not_null(episode_details['episode_status'])},
                        {"dataElement": data_element_mapping['adherence_string'], "value": assign_value_if_not_null(episode_details['adherence_string'])}
                    ]
                }
                update_events_in_dhis2(existing_event[0]['event'],event_payload, device_imei, episode_id )
            
            else:
                event_payload = {
                    "program": program_uid,
                    "orgUnit": orgUnit,
                    "eventDate": format_date(episode_details['episode_start_date']),
                    "programStage": program_stage,
                    "status": "ACTIVE",
                    "trackedEntityInstance": tei_uid,
                    "dataValues": [
                        {"dataElement": data_element_mapping['episode_id'], "value": assign_value_if_not_null(episode_details['episode_id'])},
                        {"dataElement": data_element_mapping['episode_status'], "value": assign_value_if_not_null(episode_details['episode_status'])},
                        {"dataElement": data_element_mapping['last_battery_level'], "value": assign_value_if_not_null(episode_details['last_battery_level'])},
                        {"dataElement": data_element_mapping['total_device_days'], "value": assign_value_if_not_null(episode_details['total_device_days'])},
                        {"dataElement": data_element_mapping['total_device_dose_days'], "value": assign_value_if_not_null(episode_details['total_device_dose_days'])},
                        {"dataElement": data_element_mapping['total_episode_days'], "value": assign_value_if_not_null(episode_details['total_episode_days'])},
                        {"dataElement": data_element_mapping['Calendar'], "value": assign_value_if_not_null(episode_details['Calendar'])},
                        {"dataElement": data_element_mapping['episode_end_date'], "value": assign_value_if_not_null(episode_details['episode_end_date'])},
                        {"dataElement": data_element_mapping['episode_start_date'], "value": assign_value_if_not_null(episode_details['episode_start_date'])},
                        {"dataElement": data_element_mapping['last_seen'], "value": assign_value_if_not_null(episode_details['last_seen'])},
                        {"dataElement": data_element_mapping['last_signal_strength'], "value": assign_value_if_not_null(episode_details['last_signal_strength'])},
                        {"dataElement": data_element_mapping['last_opened'], "value": assign_value_if_not_null(episode_details['last_opened'])},
                        {"dataElement": data_element_mapping['episode_status'], "value": assign_value_if_not_null(episode_details['episode_status'])},
                        {"dataElement": data_element_mapping['adherence_string'], "value": assign_value_if_not_null(episode_details['adherence_string'])}
                    ]
                }
                push_events_in_dhis2(event_payload, device_imei, episode_id )
            
            #print(f"episode_details. episode_id : {episode_id} . device_imei : {device_imei} . episode_start_date : {episode_start_date}")
            #print(f"episode_details. adherence_string : {adherence_string} . Calendar : {Calendar} . last_seen : {last_seen}")


def push_events_in_dhis2(event_payload, device_imei, episode_id ):
    #
    try:
        response = session.post(event_endpoint, data=json.dumps(event_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        #print('####################################################### SUCCESSFUL ##########################################################', flush=True)
        #print(f'RECORD NO.: {record_count}   current benID: {row["BeneficiaryRegID"]}', flush=True)
        event_uid = response.json().get("response", {}).get("importSummaries", [])[0].get("reference")
        #event_ids = [item.get("event") for item in response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")]
        #print(f"Events created successfully. Event IDs: {response.json()}")
        event_count = response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")
        print(f"Events created successfully. device_imei : {device_imei} . episode_id : {episode_id} Event count: {event_count}. imported event : {event_uid}")
        logging.info(f"Events created successfully. device_imei : {device_imei} . episode_id : {episode_id} .Event count: {event_count}. imported event : {event_uid}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        #print(f'####################################################### FAILED #######################################################', flush=True)
        #print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
        print(f"Failed to create events. Error: {response.text}")
        logging.error(f"Failed to create events .device_imei : {device_imei} . episode_id : {episode_id} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

        with open(LOG_FILE_WISEPILL_EVENT_ERROR_LOG, 'a') as fail_record:
            fail_record.write(f'\ncurrent device_imei: {device_imei}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f"Failed to create events. Error: {response.text}")
        logging.error(f"Failed to create events . device_imei : {device_imei} . episode_id : {episode_id} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

def update_events_in_dhis2(event_uid,event_payload, device_imei, episode_id ):
    #
    
    event_update_endpoint = f"{event_endpoint}/{event_uid}"
    #print(f"event_update_endpoint: {event_update_endpoint}")
    try:
        response = session.put(event_update_endpoint, data=json.dumps(event_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        #print('####################################################### SUCCESSFUL ##########################################################', flush=True)
        #print(f'RECORD NO.: {record_count}   current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Events updated successfully.: {response.text}")
        #logging.error(f"Events updated successfully.: {response.text}")

        #event_uid = response.json().get("response", {}).get("importSummaries", [])[0].get("reference")
        #event_ids = [item.get("event") for item in response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")]
        #print(f"Events created successfully. Event IDs: {response.json()}")
        #event_count = response.json().get("response", {}).get("importSummaries", [])[0].get("importCount",{}).get("imported")
        
        impCount = response.json().get("response", {}).get("importCount", {}).get("imported")
        updatedCount = response.json().get("response", {}).get("importCount", {}).get("updated")
        ignoreCount = response.json().get("response", {}).get("importCount", {}).get("ignored")
        print(f"Events updated successfully. device_imei : {device_imei} . episode_id : {episode_id} update event count: {updatedCount}. imported event : {event_uid}")
        logging.info(f"Events updated successfully. device_imei : {device_imei} . episode_id : {episode_id} .update event count: {updatedCount}. imported event : {event_uid}")
    except requests.RequestException as e:
        resp_msg=response.text
        ind=resp_msg.find('conflict')
        #print(f'####################################################### FAILED #######################################################', flush=True)
        #print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        #print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
        print(f"Failed to updated events. Error: {response.text}")
        logging.error(f"Failed to updated events .device_imei : {device_imei} . episode_id : {episode_id} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")

        with open(LOG_FILE_WISEPILL_EVENT_ERROR_LOG, 'a') as fail_record:
            fail_record.write(f'\ncurrent device_imei: {device_imei}. \n Error Message: {resp_msg[ind-1:]}\n')
            fail_record.write("----------------------------------------------------------------------------------------\n")

        print(f"Failed to updated events. Error: {response.text}")
        logging.error(f"Failed to updated events . device_imei : {device_imei} . episode_id : {episode_id} . Status code: {response.status_code} . error details: {response.json()} .Error: {response.text}")


try:
    
    sql_views_data_device_imei = get_sqlview_data_device_imei()
    print( f" length of sql_views_data_device_imei data value . { len(sql_views_data_device_imei) }" )
    logging.info( f" length of sql_views_data_device_imei data value . { len(sql_views_data_device_imei) }" )
    #for index, eventDataValueRow in updateEventDataValues.iterrows():
    for index, device_imei in enumerate(sql_views_data_device_imei):
        #print(f"Row {index + 1}: {row}" )
            evrimed_wisepill_episodes = get_evrimed_wisepill_episodes( device_imei[0] )
            #print(f"evrimed_wisepill_episodes size {len(evrimed_wisepill_episodes)}")
            add_update_event(evrimed_wisepill_episodes)
        
    
except Exception as e:
    logging.error(f"Error: {str(e)}")


current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print( f" pushing Event finished . { current_time_end }" )
logging.info(f" pushing Event finished . { current_time_end }")





