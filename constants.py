# constants.py

from datetime import datetime

LOG_FILE_ENROLLMENT = datetime.now().strftime("%Y-%m-%d") + "_enrollment.txt"
LOG_FILE_EVENT = datetime.now().strftime("%Y-%m-%d") + "_event.txt"
LOG_FILE_DATA_VALUE_SET = datetime.now().strftime("%Y-%m-%d") + "_dataValueSet.txt"
LOG_FILE_DATA_VALUE_SET_LAST_SYNC = datetime.now().strftime("%Y-%m-%d") + "_dataValueSet_last_sync.txt"
LOG_FILE_EVENT_DATA_VALUE_UPDATE_AGE = datetime.now().strftime("%Y-%m-%d") + "_updateEventDataValue_age.txt"
LOG_FILE_EVENT_DATA_VALUE_UPDATE_SEX = datetime.now().strftime("%Y-%m-%d") + "_updateEventDataValue_sex.txt"
LOG_FILE_EVENT_DATA_VALUE_UPDATE_FSW_TYPE = datetime.now().strftime("%Y-%m-%d") + "_updateEventDataValue_fSW_type.txt"
LOG_FILE_EVENT_DATA_VALUE_UPDATE_CLIENT_OF_FSW_TYPE = datetime.now().strftime("%Y-%m-%d") + "_updateEventDataValue_client_of_fSW_type.txt"
LOG_FILE_EVENT_DATA_VALUE_UPDATE_RISK_GROUP = datetime.now().strftime("%Y-%m-%d") + "_updateEventDataValue_risk_group.txt"
LOG_FILE_EVENT_DATA_VALUE_UPDATE_MARTIAL_STATUS = datetime.now().strftime("%Y-%m-%d") + "_updateEventDataValue_marital_status.txt"



